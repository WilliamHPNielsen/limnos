"""
Test module specifically for the methods of the Trails type
"""

from limnos.types import Trails


def test_equality():

    r1 = [(1, 1), (1, 3), (3, 3)]
    t1 = Trails(r1, [])

    assert t1 != r1

    r1 = [(1, 1), (1, 3), (1, 5), (3, 5), (5, 5)]
    r2 = [(1, 3), (3, 3)]
    r3 = [(5, 5), (5, 3)]

    t1 = Trails(main=r1,
                branches=[Trails(r2, []), Trails(r3, [])])
    t2 = Trails(main=r1,
                branches=[Trails(r3, []), Trails(r2, [])])
    t3 = Trails(main=r1, branches=[])

    t4 = Trails(main=r1, branches=[])
    t4.add_branch(Trails(r2, []))
    t4.add_branch(Trails(r3, []))

    assert t1 == t2
    assert t1 != t3
    assert t2 != t3
    assert t1 == t2 == t4

    r1 = [(1, 1), (1, 3), (3, 3), (5, 3), (7, 3), (7, 5), (7, 7)]
    r2 = [(3, 3), (3, 5)]
    r3 = [(3, 3), (3, 1)]
    r4 = [(7, 5), (5, 5)]

    t1 = Trails(main=r1,
                branches=[Trails(r2, []), Trails(r3, []), Trails(r4, [])])
    t2 = Trails(main=r1,
                branches=[Trails(r2, []), Trails(r4, []), Trails(r3, [])])
    t3 = Trails(main=r1,
                branches=[Trails(r3, []), Trails(r2, []), Trails(r4, [])])
    t4 = Trails(main=r1,
                branches=[Trails(r3, []), Trails(r4, []), Trails(r2, [])])
    t5 = Trails(main=r1,
                branches=[Trails(r4, []), Trails(r2, []), Trails(r3, [])])
    t6 = Trails(main=r1,
                branches=[Trails(r4, []), Trails(r3, []), Trails(r2, [])])

    assert t1 == t2 == t3 == t4 == t5 == t6
