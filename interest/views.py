from django.shortcuts import render

# Create your views here.
# interest/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .gpt_utils import extract_keywords_by_gpt

class GPTKeywordExtractionView(APIView):
    def post(self, request):
        text = request.data.get("text")
        if not text:
            return Response({"error": "자기소개 텍스트가 필요합니다."}, status=400)

        try:
            result = extract_keywords_by_gpt(text)
            return Response({"result": result}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
