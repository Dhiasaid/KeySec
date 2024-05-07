from rest_framework import serializers


try:

    from home.models import Agents

except:
    pass 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:

        try:
            model = Agents
        except:
            pass    
        fields = '__all__'

