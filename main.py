from pydantic import BaseModel, RootModel, ValidationError


class Model1(BaseModel):
    i: int
    s: str
    ss: list[str]


# トップレベルが、オブジェクト型ではなくlistの場合は、RootModelを使う
Models = RootModel[list[Model1]]

if __name__ == '__main__':
    # model_validate_jsonでjsonをvalidateしつつModelを生成できる
    j1 = """
    {"i": 1, "s": "a", "ss": ["a", "b", "c"]}
    """
    o1 = Model1.model_validate_json(j1)
    print(o1)

    # Schemaが合わない場合、ValidationErrorが発生する
    try:
        j2 = """
        {"i": 1, "s": "a", "ss": ["a", "b", 1]}
        """
        o2 = Model1.model_validate_json(j2)
    except ValidationError as e:
        print(type(e), e)

    # RootModelのオブジェクトには、rootでアクセスできる。
    j3 = """
    [{"i": 1, "s": "a", "ss": ["a", "b", "c"]}, {"i": 2, "s": "b", "ss": ["d", "e", "f"]}]
    """
    o3 = Models.model_validate_json(j3)
    print(o3.root)
