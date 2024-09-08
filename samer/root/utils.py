from os import path
from bson import ObjectId

from samer.utils import upload_file, delete_file
from samer.posts.models import post as mongo_post, PostTypes, ParsedPost
from samer.posts.utils import (
    is_image,
    is_video,
    upload_thumbnail,
)


def rollback_posts(objects: list[str]):
    for o in objects:
        delete_file(object_name=o)


def create_post(files, name, des):
    if name is None:
        full_file_name = str(files[0].name)
        file_name, _ext = path.splitext(full_file_name)
        name = file_name
    check_post_name = mongo_post.find_one(
        query={"name": name},
    )
    if check_post_name is not None:
        return {"error": True, "status": "DuplicateName"}
    upload_video = False
    upload_image = False
    file_results = {
        "urls": [],
        "object_names": [],
    }
    for index, file in enumerate(files):
        post_bytes = file.read()
        file.seek(0)
        full_file_name = str(file.name)
        file_name, _ext = path.splitext(full_file_name)
        if is_image(post_bytes):
            if upload_video:
                rollback_posts(file_results["object_names"])
                return {
                    "error": True,
                    "status": "MixedVideoAndImage",
                }
            object_name = f"imagenes/{full_file_name}"
            uploaded_file_url = upload_file(
                file,
                object_name=object_name,
            )
            file_results["urls"].append(uploaded_file_url)
            file_results["object_names"].append(object_name)
            upload_image = True
        elif is_video(post_bytes):
            if index > 0:
                rollback_posts(file_results["object_names"])
                return {
                    "error": True,
                    "status": "MoreThanOneVideo",
                }
            if upload_image:
                rollback_posts(file_results["object_names"])
                return {
                    "error": True,
                    "status": "MixedVideoAndImage",
                }
            object_name = f"videos/{full_file_name}"
            uploaded_file_url = upload_file(
                file,
                object_name=object_name,
            )
            thumbnail = upload_thumbnail(0, uploaded_file_url)
            file_results["urls"].append(uploaded_file_url)
            file_results["object_names"].append(object_name)
            upload_video = True
        else:
            rollback_posts(file_results["object_names"])
            return {
                "error": True,
                "status": "NotImageOrVideo",
            }
    res = mongo_post.create(
        name=name,
        object_names=file_results["object_names"],
        urls=file_results["urls"],
        description=des,
        type=PostTypes.IMAGE if upload_image else PostTypes.VIDEO,
        thumbnail_url=thumbnail if upload_video else None,
    )
    return {
        "status": "Success",
        "urls": file_results["urls"],
        "id": str(res.inserted_id),
    }


def edit_post(files, name, des, post: ParsedPost):
    upload_video = False
    upload_image = False
    file_results = {
        "urls": [],
        "object_names": [],
    }
    for index, file in enumerate(files):
        post_bytes = file.read()
        file.seek(0)
        full_file_name = str(file.name)
        file_name, _ext = path.splitext(full_file_name)
        if is_image(post_bytes):
            if upload_video:
                rollback_posts(file_results["object_names"])
                return {
                    "error": True,
                    "status": "MixedVideoAndImage",
                }
            object_name = f"imagenes/{file_name}"
            uploaded_file_url = upload_file(
                file,
                object_name=object_name,
            )
            file_results["urls"].append(uploaded_file_url)
            file_results["object_names"].append(object_name)
            upload_image = True
        elif is_video(post_bytes):
            if index > 0:
                rollback_posts(file_results["object_names"])
                return {
                    "error": True,
                    "status": "MoreThanOneVideo",
                }
            if upload_image:
                rollback_posts(file_results["object_names"])
                return {
                    "error": True,
                    "status": "MixedVideoAndImage",
                }
            object_name = f"videos/{file_name}"
            uploaded_file_url = upload_file(
                file,
                object_name=object_name,
            )
            file_results["urls"].append(uploaded_file_url)
            file_results["object_names"].append(object_name)
            upload_video = True
        else:
            rollback_posts(file_results["object_names"])
            return {
                "error": True,
                "status": "NotImageOrVideo",
            }
    if len(files) != 0:
        for object_name in post["object_names"]:
            delete_file(object_name=object_name)
    description = des if des is not None else post["description"]
    type = post["type"]
    if upload_image:
        type = PostTypes.IMAGE.value
    elif upload_video:
        type = PostTypes.VIDEO.value
    res = mongo_post.update_one(
        filter={"_id": ObjectId(post["id"])},
        update={
            "$set": {
                "name": name if name is not None else post["name"],
                "object_names": (
                    file_results["object_names"]
                    if len(
                        file_results["object_names"],
                    )
                    > 0
                    else post["object_names"]
                ),
                "urls": (
                    file_results["urls"]
                    if len(
                        file_results["urls"],
                    )
                    > 0
                    else post["urls"]
                ),
                "description": description,
                "type": type,
                "thumbnail_url": (
                    upload_thumbnail(
                        0,
                        file_results["urls"][0],
                    )
                    if upload_video
                    else post["thumbnail_url"]
                ),
            }
        },
    )
    return {
        "status": "Success",
        "urls": file_results["urls"],
        "id": str(res.upserted_id) if res.upserted_id is not None else None,
    }
