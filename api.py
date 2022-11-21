import shutil
from typing import List
from fastapi import APIRouter, UploadFile, File, Form

from schemas import UploadVideo, GetVideo, Message
from models import Video

video_router = APIRouter()


@video_router.post('/')
async def root(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    info = UploadVideo(title=title, description=description)
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file_name": file.filename, "info": info}


@video_router.post('/img')
async def upload_image(files: List[UploadFile] = File(...)):
    for img in files:
        with open(f'{img.filename}', "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

    return {"file_name": "Good"}


@video_router.post("/video")
async def create_video(video: Video):
    await video.save()
    return video


@video_router.get('/video/{video_pk}', response_model=Video, responses={404: {"model": Message}})
async def get_video(video_pk: int):
    return await Video.objects.select_related("user").get(pk=video_pk)
