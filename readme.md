# Track Python Fields at Runtime and Share Methods w/o Inheritance

---
While data classes are an interesting construct in Python, they might not exactly be what you want in a specific
situation.

Let's say you have many classes, partly inherited from each other, in which attributes, so-called "fields", are defined.  
Here's an example:

```
class A:
    a: int
    b: str

class B(A):
    c: float

class C(A):
    d: str

class D(B, C):
    e: int
```

Let's assume such classes are part of a bigger data model of which you have two instances you would like to compare
at runtime in a generic way. A Python object may carry a ton of attributes. Not each and every attribute might be
relevant for comparison. Instead, you can define the fields of each class as precisely those attributes you want to have
compared. So, what you would like to have, perhaps, is a bunch of meta methods attached to each class of your data model
for fields inspection or other purposes. Instead of writing the code of these methods for every single class, or
inheriting all classes from a common base class containing these shared methods, we could simply decorate each class
with the least amount of interference. The decorator is called "adjunct" here:

```
@adjunct
class A:
    a: int
    b: str
```

If you add parameters to such a decorator, you could even customize the set of meta methods for
an individual class by deselecting certain methods, e.g. methods 4 and 6, that are undesired for some reason:

```
@adjunct(method4=False, method6=False)
class B(A):
    c: float
```

Let's say you have such a decorated class and the decorator automatically adds one meta method ```unused_fields()```
that provide you with fields - inherited ones, too! - of a class (instance) that were merely declared, and with another
meta method ```used_fields()``` that provides you with fields that have been both declared and initialized.

Now, what you could do to compare two instances of such a class in a generic way, is to call both of the above meta
methods on both instances and compare the results first before going into any deeper comparisons. Here is an example
that tracks instance fields using decorated versions of the above classes:

```
def print_fields(obj: object) -> None:
    print(f'fields: {obj._FIELDS}')
    print(f'used fields: {obj.used_fields()}')
    print(f'unused fields: {obj.unused_fields()}')

def main() -> None:
    a = dm.A()
    print_fields(a)
    b = dm.B()
    print_fields(b)
    c = dm.C()
    print_fields(c)
    d = dm.D()
    d.a = 42
    print_fields(d)
```

Executing ```main()``` yields the following output:

```
fields: {'a': <class 'int'>, 'b': <class 'str'>}
used fields: {}
unused fields: {'a': <class 'int'>, 'b': <class 'str'>}
fields: {'a': <class 'int'>, 'b': <class 'str'>, 'c': <class 'float'>}
used fields: {}
unused fields: {'a': <class 'int'>, 'b': <class 'str'>, 'c': <class 'float'>}
fields: {'a': <class 'int'>, 'b': <class 'str'>, 'd': <class 'str'>}
used fields: {}
unused fields: {'a': <class 'int'>, 'b': <class 'str'>, 'd': <class 'str'>}
fields: {'a': <class 'int'>, 'b': <class 'str'>, 'c': <class 'float'>, 'd': <class 'str'>, 'e': <class 'int'>}
used fields: {'a': <class 'int'>}
unused fields: {'b': <class 'str'>, 'c': <class 'float'>, 'd': <class 'str'>, 'e': <class 'int'>}
```
