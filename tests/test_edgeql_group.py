#
# This source file is part of the EdgeDB open source project.
#
# Copyright 2012-present MagicStack Inc. and the EdgeDB authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os.path

from edb.testbase import server as tb


class TestEdgeQLGroup(tb.QueryTestCase):
    '''These tests are focused on using the internal GROUP statement.'''

    SCHEMA = os.path.join(os.path.dirname(__file__), 'schemas',
                          'issues.esdl')

    SCHEMA_CARDS = os.path.join(os.path.dirname(__file__), 'schemas',
                                'cards.esdl')

    SETUP = os.path.join(os.path.dirname(__file__), 'schemas',
                         'groups_setup.edgeql')

    async def test_edgeql_group_simple_01(self):
        # XXX: key, also
        await self.assert_query_result(
            r'''
            GROUP cards::Card {name} BY .element
            ''',
            tb.bag([
                {
                    "elements": tb.bag(
                        [{"name": "Bog monster"}, {"name": "Giant turtle"}]),
                    "key": {"element": "Water"}
                },
                {
                    "elements": tb.bag([{"name": "Imp"}, {"name": "Dragon"}]),
                    "key": {"element": "Fire"}
                },
                {
                    "elements": tb.bag([{"name": "Dwarf"}, {"name": "Golem"}]),
                    "key": {"element": "Earth"}
                },
                {
                    "elements": tb.bag([
                        {"name": "Sprite"},
                        {"name": "Giant eagle"},
                        {"name": "Djinn"}
                    ]),
                    "key": {"element": "Air"}
                }
            ])
        )

    async def test_edgeql_group_simple_02(self):
        # XXX: key, also
        await self.assert_query_result(
            r'''
            SELECT (GROUP cards::Card {name} BY .element)
            ''',
            tb.bag([
                {
                    "elements": tb.bag(
                        [{"name": "Bog monster"}, {"name": "Giant turtle"}]),
                    "key": {"element": "Water"}
                },
                {
                    "elements": tb.bag([{"name": "Imp"}, {"name": "Dragon"}]),
                    "key": {"element": "Fire"}
                },
                {
                    "elements": tb.bag([{"name": "Dwarf"}, {"name": "Golem"}]),
                    "key": {"element": "Earth"}
                },
                {
                    "elements": tb.bag([
                        {"name": "Sprite"},
                        {"name": "Giant eagle"},
                        {"name": "Djinn"}
                    ]),
                    "key": {"element": "Air"}
                }
            ])
        )

    async def test_edgeql_group_simple_03(self):
        # XXX: key, also
        # the compilation here is kind of a bummer; could we avoid an
        # unnest?
        await self.assert_query_result(
            r'''
            SELECT (GROUP cards::Card {name} BY .element)
            FILTER .key.element != 'Air';
            ''',
            tb.bag([
                {
                    "elements": tb.bag(
                        [{"name": "Bog monster"}, {"name": "Giant turtle"}]),
                    "key": {"element": "Water"}
                },
                {
                    "elements": tb.bag([{"name": "Imp"}, {"name": "Dragon"}]),
                    "key": {"element": "Fire"}
                },
                {
                    "elements": tb.bag([{"name": "Dwarf"}, {"name": "Golem"}]),
                    "key": {"element": "Earth"}
                },
            ])
        )

    async def test_edgeql_group_simple_no_id_output_01(self):
        # the implicitly injected id was making it into the output
        # in native mode at one point
        res = await self.con.query('GROUP cards::Card {name} BY .element')
        el = tuple(tuple(res)[0].elements)[0]
        self.assertNotIn("id := ", str(el))

    async def test_edgeql_group_simple_unused_alias_01(self):
        await self.con.query('''
            WITH MODULE cards
            SELECT (
              GROUP Card
              USING x := count(.owners), nowners := x,
              BY CUBE (.element, nowners)
            )
        ''')

    async def test_edgeql_group_process_select_01(self):
        await self.assert_query_result(
            r'''
            WITH MODULE cards
            SELECT (GROUP Card BY .element) {
                element := .key.element,
                cnt := count(.elements),
            };
            ''',
            tb.bag([
                {"cnt": 2, "element": "Water"},
                {"cnt": 2, "element": "Fire"},
                {"cnt": 2, "element": "Earth"},
                {"cnt": 3, "element": "Air"}
            ])
        )

    async def test_edgeql_group_process_select_02(self):
        await self.assert_query_result(
            r'''
            WITH MODULE cards
            SELECT (GROUP Card BY .element) {
                element := .key.element,
                cnt := count(.elements),
            } FILTER .element != 'Water';
            ''',
            tb.bag([
                {"cnt": 2, "element": "Fire"},
                {"cnt": 2, "element": "Earth"},
                {"cnt": 3, "element": "Air"},
            ])
        )

    async def test_edgeql_group_process_select_03(self):
        await self.assert_query_result(
            r'''
            WITH MODULE cards
            SELECT (GROUP Card BY .element) {
                element := .key.element,
                cnt := count(.elements),
            } ORDER BY .element;
            ''',
            [
                {"cnt": 3, "element": "Air"},
                {"cnt": 2, "element": "Earth"},
                {"cnt": 2, "element": "Fire"},
                {"cnt": 2, "element": "Water"},
            ]
        )

    async def test_edgeql_group_process_for_01a(self):
        await self.assert_query_result(
            r'''
            WITH MODULE cards
            FOR g IN (GROUP Card BY .element) UNION (
                element := g.key.element,
                cnt := count(g.elements),
            );
            ''',
            tb.bag([
                {"cnt": 2, "element": "Water"},
                {"cnt": 2, "element": "Fire"},
                {"cnt": 2, "element": "Earth"},
                {"cnt": 3, "element": "Air"},
            ])
        )

    async def test_edgeql_group_process_for_01b(self):
        await self.assert_query_result(
            r'''
            WITH MODULE cards
            FOR g IN (SELECT (GROUP Card BY .element)) UNION (
                element := g.key.element,
                cnt := count(g.elements),
            );
            ''',
            tb.bag([
                {"cnt": 2, "element": "Water"},
                {"cnt": 2, "element": "Fire"},
                {"cnt": 2, "element": "Earth"},
                {"cnt": 3, "element": "Air"}
            ])
        )

    async def test_edgeql_group_sets_01(self):
        await self.assert_query_result(
            r'''
            WITH MODULE cards
            GROUP Card {name}
            USING nowners := count(.owners)
            BY {.element, nowners};
            ''',
            tb.bag([
                {
                    "elements": [
                        {"name": "Bog monster"}, {"name": "Giant turtle"}],
                    "grouping": ["element"],
                    "key": {"element": "Water", "nowners": None}
                },
                {
                    "elements": [{"name": "Dragon"}, {"name": "Imp"}],
                    "grouping": ["element"],
                    "key": {"element": "Fire", "nowners": None}
                },
                {
                    "elements": [{"name": "Dwarf"}, {"name": "Golem"}],
                    "grouping": ["element"],
                    "key": {"element": "Earth", "nowners": None}
                },
                {
                    "elements": [
                        {"name": "Djinn"},
                        {"name": "Giant eagle"},
                        {"name": "Sprite"},
                    ],
                    "grouping": ["element"],
                    "key": {"element": "Air", "nowners": None}
                },
                {
                    "elements": [{"name": "Golem"}],
                    "grouping": ["nowners"],
                    "key": {"element": None, "nowners": 3}
                },
                {
                    "elements": [
                        {"name": "Bog monster"}, {"name": "Giant turtle"}],
                    "grouping": ["nowners"],
                    "key": {"element": None, "nowners": 4}
                },
                {
                    "elements": [
                        {"name": "Djinn"},
                        {"name": "Dragon"},
                        {"name": "Dwarf"},
                        {"name": "Giant eagle"},
                        {"name": "Sprite"},
                    ],
                    "grouping": ["nowners"],
                    "key": {"element": None, "nowners": 2}
                },
                {
                    "elements": [{"name": "Imp"}],
                    "grouping": ["nowners"],
                    "key": {"element": None, "nowners": 1}
                }
            ]),
            sort={'elements': lambda x: x['name']},
        )

    async def test_edgeql_group_sets_02(self):
        # XXX: this breaks when

        await self.assert_query_result(
            r'''
            WITH MODULE cards
            GROUP Card
            USING nowners := count(.owners)
            BY {.element, nowners};
            ''',
            tb.bag([
                {
                    "elements": [{"id": str}] * 2,
                    "grouping": ["element"],
                    "key": {"element": "Water", "nowners": None}
                },
                {
                    "elements": [{"id": str}] * 2,
                    "grouping": ["element"],
                    "key": {"element": "Fire", "nowners": None}
                },
                {
                    "elements": [{"id": str}] * 2,
                    "grouping": ["element"],
                    "key": {"element": "Earth", "nowners": None}
                },
                {
                    "elements": [{"id": str}] * 3,
                    "grouping": ["element"],
                    "key": {"element": "Air", "nowners": None}
                },
                {
                    "elements": [{"id": str}] * 1,
                    "grouping": ["nowners"],
                    "key": {"element": None, "nowners": 3}
                },
                {
                    "elements": [{"id": str}] * 2,
                    "grouping": ["nowners"],
                    "key": {"element": None, "nowners": 4}
                },
                {
                    "elements": [{"id": str}] * 5,
                    "grouping": ["nowners"],
                    "key": {"element": None, "nowners": 2}
                },
                {
                    "elements": [{"id": str}] * 1,
                    "grouping": ["nowners"],
                    "key": {"element": None, "nowners": 1}
                }
            ]),
        )

    async def test_edgeql_group_grouping_sets_01(self):
        res = [
            {"grouping": [], "num": 9},
            {"grouping": ["element"], "num": int},
            {"grouping": ["element"], "num": int},
            {"grouping": ["element"], "num": int},
            {"grouping": ["element"], "num": int},
            {"grouping": ["element", "nowners"], "num": int},
            {"grouping": ["element", "nowners"], "num": int},
            {"grouping": ["element", "nowners"], "num": int},
            {"grouping": ["element", "nowners"], "num": int},
            {"grouping": ["element", "nowners"], "num": int},
            {"grouping": ["element", "nowners"], "num": int},
            {"grouping": ["nowners"], "num": int},
            {"grouping": ["nowners"], "num": int},
            {"grouping": ["nowners"], "num": int},
            {"grouping": ["nowners"], "num": int},
        ]

        await self.assert_query_result(
            r'''
            WITH MODULE cards
            SELECT (
              GROUP Card
              USING nowners := count(.owners)
              BY CUBE (.element, nowners)
            ) {
                num := count(.elements),
                grouping
            } ORDER BY .grouping;
            ''',
            res
        )

        # With an extra SELECT
        await self.assert_query_result(
            r'''
            WITH MODULE cards
            SELECT (SELECT (
              GROUP Card
              USING nowners := count(.owners)
              BY CUBE (.element, nowners)
            ) {
                num := count(.elements),
                grouping
            }) ORDER BY .grouping;
            ''',
            res
        )

        await self.assert_query_result(
            r'''
            WITH MODULE cards
            SELECT (
              GROUP Card
              USING x := count(.owners), nowners := x,
              BY CUBE (.element, nowners)
            ) {
                num := count(.elements),
                grouping
            } ORDER BY .grouping;
            ''',
            res
        )

    async def test_edgeql_group_grouping_sets_02(self):
        # we just care about the grouping names we generate
        await self.assert_query_result(
            r'''
            WITH MODULE cards
            SELECT (
              WITH W := (SELECT Card { name } LIMIT 1)
              GROUP W
              USING nowners := count(.owners)
              BY CUBE (.element, .cost, nowners)
            ) { grouping } ORDER BY (len(.grouping), .grouping);
            ''',
            [
                {"grouping": []},
                {"grouping": ["cost"]},
                {"grouping": ["element"]},
                {"grouping": ["nowners"]},
                {"grouping": ["cost", "nowners"]},
                {"grouping": ["element", "cost"]},
                {"grouping": ["element", "nowners"]},
                {"grouping": ["element", "cost", "nowners"]}
            ]
            # XXX: or a sorted version?
            # [
            #     {"grouping": []},
            #     {"grouping": ["cost"]},
            #     {"grouping": ["element"]},
            #     {"grouping": ["nowners"]},
            #     {"grouping": ["cost", "element"]},
            #     {"grouping": ["cost", "nowners"]},
            #     {"grouping": ["element", "nowners"]},
            #     {"grouping": ["cost", "element", "nowners"]}
            # ]
        )

    async def test_edgeql_group_for_01(self):
        await self.assert_query_result(
            r'''
            WITH MODULE cards
            FOR g in (GROUP Card BY .element) UNION (
                WITH U := g.elements,
                SELECT U {
                    name,
                    cost_ratio := .cost / math::mean(g.elements.cost)
            });
            ''',
            tb.bag([
                {"cost_ratio": 0.42857142857142855, "name": "Sprite"},
                {"cost_ratio": 0.8571428571428571, "name": "Giant eagle"},
                {"cost_ratio": 1.7142857142857142, "name": "Djinn"},
                {"cost_ratio": 0.5, "name": "Dwarf"},
                {"cost_ratio": 1.5, "name": "Golem"},
                {"cost_ratio": 0.3333333333333333, "name": "Imp"},
                {"cost_ratio": 1.6666666666666667, "name": "Dragon"},
                {"cost_ratio": 0.8, "name": "Bog monster"},
                {"cost_ratio": 1.2, "name": "Giant turtle"}
            ])
        )
