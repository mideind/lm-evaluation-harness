from lm_eval.api.filter import Filter
from lm_eval.api.instance import Instance
from lm_eval.api.registry import get_model, register_filter
import os


@register_filter("lm_judge")
class LMJudge(Filter):
    def __init__(self, model: str, model_args: str, judge_prompt: str) -> None:
        self.model = model
        self.model_args = model_args
        self.judge_prompt = judge_prompt

        assert model in ["openai-chat-completions"]
        os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY_JUDGE"]

        self.lm = get_model(model).create_from_arg_string(
            model_args,
            {
                "batch_size": 1,
                "max_batch_size": 1,
                "device": "cpu",
            },
        )
        self.reqtype = "generate_until"

    def apply(self, resps, docs):
        resps = [
            Instance(
                request_type="generate_until",
                doc=None,
                arguments=(
                    self.judge_prompt.format(**doc | {"response": answer_list[0]}),
                    {"max_gen_toks": 200},
                ),
                idx=i,
            )
            for i, (answer_list, doc) in enumerate(zip(resps, docs))
        ]

        judge_resps = getattr(self.lm, self.reqtype)(resps)
        return [[x] for x in judge_resps]
