# 自定义 resolver

一个 resolver 就是一个函数：

```python
def resolve(paper, cfg, client) -> str:
    """返回可直接下载的 PDF URL，拿不到就返回空串。"""
```

- `paper` 是 `litpipe.model.Paper`，有 `doi` / `arxiv_id` / `title` / `url` 等字段
- `cfg` 是 `litpipe.config.Config`，用 `cfg.section("resolve")` 取自己那段配置
- `client` 是限速过的 `requests.Session` 封装，用 `client.get()` / `client.get_json()`

写好之后在 `run.py` 启动前注册，并把名字加进 `settings.yaml` 的 `resolve.chain`：

```python
from litpipe import resolvers
from mymodule import resolve as my_resolve

resolvers.register("my_source", my_resolve)
```

链条按 `resolve.chain` 的顺序走，第一个返回非空的就停，所以把成功率高、
成本低的放前面。resolver 抛异常不会中断管道，只会被跳过并打印一行。
