from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Location
from .serializers import LocationSerializer

class LocationGeoJSONView(APIView):
    def get(self, request):
        locations = Location.objects.all()
        features = []

        for loc in locations:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [loc.longitude, loc.latitude],
                },
                "properties": {
                    "name": loc.name,
                    "category": loc.category
                }
            })

        geojson = {
            "type": "FeatureCollection",
            "features": features
        }

        return Response(geojson)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import Location

class LocationStatsView(APIView):
    def get(self, request):
        total_locations = Location.objects.count()
        most_common = (
            Location.objects
            .values('category')
            .annotate(count=Count('category'))
            .order_by('-count')
            .first()
        )
        
        data = {
            "total_locations": total_locations,
            "most_common_category": most_common['category'] if most_common else None,
            "most_common_count": most_common['count'] if most_common else 0,
        }
        return Response(data)
class CategoryStatsView(APIView):
    def get(self, request):
        stats = Location.objects.values('category').annotate(count=Count('category'))
        data = {item['category']: item['count'] for item in stats}
        return Response(data)
# Create your views here.
def index(request):
    return render(request, 'index.html')