from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.account.serializers import CustomUserDeatilSerializer
from apps.cyberdoc.models import TypeConsultation, QualificationAuthor, Shrift, Guarantee, OrderWork, OrderWorkReview, \
    DescribeProblem, OrderWorkFiles


class OrderWorkFileSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderWorkFiles
        fields = '__all__'


class TypeConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeConsultation
        fields = '__all__'


class QualificationAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualificationAuthor
        fields = '__all__'


class ShriftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shrift
        fields = '__all__'


class GuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantee
        fields = '__all__'


class OrderWorkSerializer(serializers.ModelSerializer):
    type_cons = TypeConsultationSerializer()
    qualification_author = QualificationAuthorSerializer()
    shrift = ShriftSerializer()
    guarantee = GuaranteeSerializer()
    author = CustomUserDeatilSerializer()
    rating = serializers.SerializerMethodField()
    review_list = serializers.SerializerMethodField()
    files = OrderWorkFileSizeSerializer(many=True, read_only=True)

    class Meta:
        model = OrderWork
        fields = ['id', 'number_of_order', 'type_cons', 'item', 'theme', 'min_page_size',
                  'number_of_sources_literature', 'deadline', 'qualification_author',
                  'shrift', 'guarantee', 'text', 'files', 'author', 'rating', 'review_list', 'foreign_sources']

    def get_rating(self, obj):
        reviews = OrderWorkReview.objects.select_related('order_work').filter(order_work=obj)
        if reviews.exists():
            total_rating = sum([review.rating for review in reviews])
            return total_rating / reviews.count()
        return 0

    def get_review_list(self, obj):
        reviews = OrderWorkReview.objects.select_related('order_work').filter(order_work=obj)
        serializer = OrderWorkReviewSerializer(reviews, many=True)
        return serializer.data


class OrderWorkCreateAndUpdateSerializer(serializers.ModelSerializer):
    type_cons = serializers.PrimaryKeyRelatedField(queryset=TypeConsultation.objects.all())
    qualification_author = serializers.PrimaryKeyRelatedField(queryset=QualificationAuthor.objects.all())
    shrift = serializers.PrimaryKeyRelatedField(queryset=Shrift.objects.all())
    guarantee = serializers.PrimaryKeyRelatedField(queryset=Guarantee.objects.all())
    files = OrderWorkFileSizeSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(allow_empty_file=True, use_url=False),
        write_only=True
    )

    class Meta:
        model = OrderWork
        fields = [
            'id', 'type_cons', 'item', 'theme', 'min_page_size',
            'number_of_sources_literature', 'deadline', 'qualification_author',
            'shrift', 'guarantee', 'text', 'uploaded_files', 'files', 'foreign_sources'
        ]

    def create(self, validated_data):
        author = self.context['request'].user
        uploaded_files = validated_data.pop("uploaded_files", [])
        order_work = OrderWork.objects.create(
            author=author,
            **validated_data
        )
        for file in uploaded_files:
            OrderWorkFiles.objects.create(order_work=order_work, file=file)

        return order_work

    def update(self, instance, validated_data):
        type_cons_data = validated_data.pop('type_cons', None)
        qualification_author_data = validated_data.pop('qualification_author', None)
        shrift_data = validated_data.pop('shrift', None)
        guarantee_data = validated_data.pop('guarantee', None)

        if type_cons_data:
            type_cons = TypeConsultation.objects.get(id=type_cons_data)
            instance.type_cons = type_cons

        if qualification_author_data:
            qualification_author = QualificationAuthor.objects.get(id=qualification_author_data)
            instance.qualification_author = qualification_author

        if shrift_data:
            shrift = Shrift.objects.get(id=shrift_data)
            instance.shrift = shrift

        if guarantee_data:
            guarantee = Guarantee.objects.get(id=guarantee_data)
            instance.guarantee = guarantee

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class OrderWorkReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderWorkReview
        fields = ('id', 'rating', 'text', 'order_work', 'created_at')
        read_only_fields = ('created_at',)

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Оценка должна быть от 1 до 5.")
        return value


class DescribeProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescribeProblem
        fields = ['id', 'text', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        user = self.context.get('request').user

        validated_data.pop('user', None)

        create_problem = DescribeProblem.objects.create(
            user=user,
            **validated_data
        )
        return create_problem


class DescribeProblemListSerializer(serializers.ModelSerializer):
    user = CustomUserDeatilSerializer()
    
    class Meta:
        model = DescribeProblem
        fields = ['id', 'text', 'user', 'created_at']
