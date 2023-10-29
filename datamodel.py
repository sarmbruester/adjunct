
from adjunct import adjunct


@adjunct
class A:
    a: int
    b: str


@adjunct
class B(A):
    c: float


@adjunct
class C(A):
    d: str


@adjunct
class D(B, C):
    e: int
