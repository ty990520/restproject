from rest_framework import viewsets
from .models import Essay, Album, Files
from .serializers import EssaySerializer, AlbumSerializer, FilesSerializer
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser

class PostViewSet(viewsets.ModelViewSet):
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer

    filter_backends = [SearchFilter]    #검색기능(필터)
    search_fields = ('title','body')    #튜플로서 작성

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # 현재 request를 보낸 유저
    # == self.request.user


    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:  #유저가 로그인한 상태라면
            qs = qs.filter(author = self.request.user)  #해당 유저의 글을 필터링
        else:   #로그인하지 않은 경우에
            qs = qs.none()  #비어있는 쿼리셋 반환
        return qs

class ImgViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

from rest_framework.response import Response
from rest_framework import status
   
class FileViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

    #파일업로드 오류를 해결하기 위해서
    # parser_class 지정
    parser_classes = (MultiPartParser, FormParser)

    # create() 오버라이딩   #create() -> post()
    # API HTTP -> get() post()와 유사한 과정

    def post(self, request, *args, **kwargs):
        serializer = FilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)


