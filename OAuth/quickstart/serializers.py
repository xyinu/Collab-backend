from rest_framework import serializers
from .models import PO, POdetail, User, ContainerDetail, Container, insides, SKU
from django.utils import timezone, dateformat
from django.db.models import Q


class POdetailSerializer(serializers.ModelSerializer):
    SKU = serializers.CharField(source='SKU.skuID')
    total_qty = serializers.IntegerField(source='SKU.qty')
    price = serializers.FloatField(source='SKU.price')
    frombacklog = serializers.IntegerField(source='OQOUTSTAND')
    safety_qty = serializers.SerializerMethodField()

    def get_safety_qty(self, obj):
        return obj.SKU.qty//3

    class Meta:
        model = POdetail
        fields = ['SKU', 'total_qty', 'safety_qty', 'price',
                  'jpn_qty', 'promo_qty', 'demand_qty', 'frombacklog',  'remark']


class POdetailbacklogSerializer(serializers.ModelSerializer):
    SKU = serializers.CharField(source='SKU.skuID')
    total_qty = serializers.IntegerField(source='SKU.qty')
    price = serializers.FloatField(source='SKU.price')
    safety_qty = serializers.SerializerMethodField()
    qty_backlogged = serializers.IntegerField(source='OQORDERED')

    def get_safety_qty(self, obj):
        return obj.SKU.qty//3

    class Meta:
        model = POdetail
        fields = ['SKU', 'total_qty', 'safety_qty', 'price', 'qty_backlogged'
                  ]


class PObacklogSerializer(serializers.ModelSerializer):
    POdetail = POdetailbacklogSerializer(source='PO', many=True)
    VendorID = serializers.CharField(source='Vendor.vendorID')
    name = serializers.CharField(source='User.name')

    class Meta:
        model = PO
        fields = ['PONUMBER', 'VendorID', 'name',
                  'editDate', 'status', 'POdetail']


class POSerializer(serializers.ModelSerializer):
    POdetail = POdetailSerializer(source='PO', many=True)
    VendorID = serializers.CharField(source='Vendor.vendorID')
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        if(obj.User == None):
            return 'new'
        else:
            return obj.User.name

    def update(self, instance, validated_data, name):

        def dp(Asize, target, values, find, sizes):
            for r in range(1, target+1):
                for c in range(1, Asize+1):
                    values[r][c] = values[r][c-1]
                    if(sizes[c-1][0] <= r):
                        if(values[r][c] < values[r-sizes[c-1][0]][c-1]+sizes[c-1][0]):
                            values[r][c] = values[r - sizes[c-1]
                                                  [0]][c-1]+sizes[c-1][0]
                            find[r][c] = 1
            return values[target][Asize]

        def findpath(Asize, target, find, sizes):
            b = Asize
            c = target
            result = []
            while(b != 0 and c != 0):
                if(find[c][b] == 1):
                    result.append(b-1)
                    c = c-sizes[b-1][0]
                    b = b-1
                else:
                    b -= 1
            return result

        po_details = validated_data.pop('POdetail')
        instance.User = User.objects.get(name=name)
        instance.editDate = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        instance.save()
        totalsize = 0
        sizes = []
        for po_data in po_details:
            po_detail = POdetail.objects.get(
                Q(PO__PONUMBER=validated_data['PONUMBER']) & Q(PO__status=validated_data['status']) & Q(PO__Version=validated_data['Version']) & Q(SKU__skuID=po_data['SKU']))
            po_detail.jpn_qty = po_data.get('jpn_qty', po_detail.jpn_qty)
            po_detail.promo_qty = po_data.get('promo_qty', po_detail.promo_qty)
            po_detail.demand_qty = po_data.get(
                'demand_qty', po_detail.demand_qty)
            po_detail.OQOUTSTAND = po_data.get(
                'frombacklog', po_detail.OQOUTSTAND)
            po_detail.remark = po_data.get(
                'remark', po_detail.remark)
            po_detail.save()
            totalsize += int(po_detail.OQORDERED*po_detail.SKU.size*10)
            for i in range(po_detail.OQORDERED):
                sizes.append([int(po_detail.SKU.size*10), po_detail.SKU.skuID])
        while totalsize > 0:
            if(totalsize >= 680):
                temp = ContainerDetail.objects.create(
                    container=Container.objects.get(size=68), PO=instance)
                size = len(sizes)
                target = 680
                values = [[0 for i in range(size+1)] for j in range(target+1)]
                find = [[0 for i in range(size+1)] for j in range(target+1)]
                minus = dp(size, target, values, find, sizes)
                index = findpath(size, target, find, sizes)
                totalsize -= minus
                for u in index:
                    inside = insides.objects.get_or_create(
                        sku=SKU.objects.get(skuID=sizes[u][1], vendor=instance.Vendor), container=temp
                    )
                    inside[0].qty = inside[0].qty+1
                    del sizes[u]
                    inside[0].save()
                temp.save()
            elif(totalsize > 580):
                temp = ContainerDetail.objects.create(
                    container=Container.objects.get(size=68), PO=instance)
                totalsize = 0
                size = len(sizes)
                target = 680
                values = [[0 for i in range(size+1)] for j in range(target+1)]
                find = [[0 for i in range(size+1)] for j in range(target+1)]
                minus = dp(size, target, values, find, sizes)
                index = findpath(size, target, find, sizes)
                for u in index:
                    inside = insides.objects.get_or_create(
                        sku=SKU.objects.get(skuID=sizes[u][1], vendor=instance.Vendor), container=temp
                    )
                    inside[0].qty += 1
                    del sizes[u]
                    inside[0].save()
                temp.save()
            elif(totalsize > 280):
                temp = ContainerDetail.objects.create(
                    container=Container.objects.get(size=58), PO=instance)
                totalsize = 0
                size = len(sizes)
                target = 580
                values = [[0 for i in range(size+1)] for j in range(target+1)]
                find = [[0 for i in range(size+1)] for j in range(target+1)]
                minus = dp(size, target, values, find, sizes)
                index = findpath(size, target, find, sizes)
                for u in index:
                    inside = insides.objects.get_or_create(
                        sku=SKU.objects.get(skuID=sizes[u][1], vendor=instance.Vendor), container=temp
                    )
                    inside[0].qty += 1
                    del sizes[u]
                    inside[0].save()
                temp.save()
            else:
                temp = ContainerDetail.objects.create(
                    container=Container.objects.get(size=28), PO=instance)
                totalsize = 0
                size = len(sizes)
                target = 280
                values = [[0 for i in range(size+1)] for j in range(target+1)]
                find = [[0 for i in range(size+1)] for j in range(target+1)]
                minus = dp(size, target, values, find, sizes)
                index = findpath(size, target, find, sizes)
                for u in index:
                    inside = insides.objects.get_or_create(
                        sku=SKU.objects.get(skuID=sizes[u][1], vendor=instance.Vendor), container=temp
                    )
                    inside[0].qty += 1
                    del sizes[u]
                    inside[0].save()
                temp.save()
        return instance

    class Meta:
        model = PO
        fields = ['PONUMBER', 'VendorID', 'name',
                  'editDate', 'status', 'Version', 'POdetail']


class insidecontainerSerializer(serializers.ModelSerializer):
    SKU = serializers.CharField(source='sku.skuID')
    total_size = serializers.SerializerMethodField()

    def get_total_size(self, obj):
        return round(obj.qty*obj.sku.size, 1)

    class Meta:
        model = insides
        fields = ['SKU', 'qty', 'total_size']


class ContainerDetailSerializer(serializers.ModelSerializer):
    Content = insidecontainerSerializer(source='insidecontain', many=True)
    length = serializers.CharField(source='container.dimension')
    volume = serializers.IntegerField(source='container.size')
    PO_id = serializers.CharField(source='PO.PONUMBER')
    con_id = serializers.IntegerField(source='pk')
    capacity = serializers.FloatField(source='percentfilled')
    volume_left = serializers.SerializerMethodField()

    def get_volume_left(self, obj):
        insides = obj.insidecontain.all()
        k = 0
        for i in insides:
            k += i.qty*i.sku.size
        return round(obj.volume-k, 1)

    class Meta:
        model = ContainerDetail
        fields = ['con_id', 'PO_id', 'length',
                  'volume', 'capacity', 'Content']


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'name', 'password',
                  'user_type']


class SKUSerializer(serializers.ModelSerializer):
    vendorID = serializers.CharField(source='vendor.vendorID')

    class Meta:
        model = SKU
        fields = ['skuID', 'description', 'vendorID', 'status', 'category']
