import json
from pathlib import Path

import numpy as np

from utils.config import ensure_plugin_config_from_template

__TEMPLATE_PATH = Path(__file__).with_name("blind_box_data_template.json")


def load_blind_box_data():
    path = ensure_plugin_config_from_template(
        "kmrp-blind_box",
        "blind_box_data.json",
        __TEMPLATE_PATH,
    )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def random_get_box(blind_box_name: str, blind_box_count: int):
    blind_box_data = load_blind_box_data()
    if blind_box_data.get(blind_box_name) is None:
        return None
    bonus_info = {"gift": []}
    cur_blind_box = blind_box_data[blind_box_name]
    unit = cur_blind_box["unit"]
    total_price = float(cur_blind_box["price"]) * blind_box_count
    earn_price = 0

    weights = [int(i["weight"]) for i in cur_blind_box["bonus"]]
    elements = [i for i in range(len(cur_blind_box["bonus"]))]

    samples = np.random.choice(elements, size=blind_box_count, p=np.array(weights) / np.sum(weights))
    unique, counts = np.unique(samples, return_counts=True)
    result = dict(zip(unique, counts))
    for idx in unique:
        count = result[idx]
        price = count * float(cur_blind_box["bonus"][idx]["price"])
        earn_price += price
        bonus_info["gift"].append({
            "name": cur_blind_box["bonus"][idx]["name"],
            "count": count,
            "price": round(price, 2)
        })
    bonus_info["price"] = {
        "total": round(total_price, 2),
        "earn": round(earn_price, 2),
        "win": round(earn_price - total_price, 2),
        "unit": unit
    }
    return bonus_info
