import argparse

from .api import serve

p = argparse.ArgumentParser(prog="tutorias")
p.add_argument("--port", type=int, default=8000)
p.add_argument("--db", default="tutorias.db")
a = p.parse_args()
serve(a.port, a.db)
