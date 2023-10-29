
import datamodel as dm


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


if __name__ == '__main__':
    main()
