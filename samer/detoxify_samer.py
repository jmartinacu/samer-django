from typing import TypedDict

from detoxify import Detoxify

detoxify = Detoxify("multilingual")


class KeyDetoxify(TypedDict):
    toxic: bool
    info: list[tuple[str, float]]


class ReturnDetoxify(TypedDict):
    toxicity: KeyDetoxify
    severe_toxicity: KeyDetoxify
    identity_attack: KeyDetoxify
    insult: KeyDetoxify
    threat: KeyDetoxify
    sexual_explicit: KeyDetoxify


def predict_detoxify(data) -> ReturnDetoxify:
    result = {}
    detoxify_result = detoxify.predict(data)
    for key in detoxify_result:
        if key == "obscene":
            continue
        result[key] = {"toxic": False, "info": []}
        toxic = list(
            filter(
                lambda v: v[1] >= 0.09,
                enumerate(detoxify_result[key]),
            )
        )
        if len(toxic) != 0:
            result[key]["toxic"] = True
            result[key]["info"] = [(data[index], t) for index, t in toxic]
    return result
