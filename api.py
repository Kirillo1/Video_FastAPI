import shutil
from fastapi import (APIRouter, UploadFile, File, Form,
                     HTTPException, BackgroundTasks)
from starlette.templating import Jinja2Templates
from schemas import UploadVideo, GetVideo, Message
from models import Video, User
from services import write_video

video_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@video_router.post('/')
async def create_video(
        background_task: BackgroundTasks,
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...),
):
    file_name = f'media/{file.filename}'
    if file.content_type == 'video/mp4':
        background_task.add_task(write_video, file_name, file)
    else:
        raise HTTPException(status_code=419, detail='It is npt mp4')
    info = UploadVideo(title=title, description=description)
    user = await User.objects.first()
    return await Video.objects.create(file=file_name, user=user, **info.dict())


# @video_router.post("/video")
# async def create_video_1(video: Video):
#     await video.save()
#     return video


@video_router.get('/video/{video_pk}', response_model=GetVideo, responses={404: {"model": Message}})
async def get_video(video_pk: int):
    return await Video.objects.select_related("user").get(pk=video_pk)
