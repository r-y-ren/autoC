# Strategy: Use the inspected Pipe-16 HybridOpening controller. Reassign idle workers during the first three days to plant, water and harvest one temporary wheat crop, then restore the planned pasture and deliver the wheat. Preserve the public Metav4 production and market controller. This is attributed reuse, and its stronger public source still needs live confirmation. Disable optional environment-dependent external library loading so the archive is self-contained.
# Local packaging modifications, 2026-09-20. Original attribution retained.
# Kaggriculture submission v9/3: public V39 (Apache-2.0, notices below) plus the v9 layers
# RACEPX gate, RACE (reservation from step 192, horizon 40 / margin 12), COURIER, CARROT and HERD
# appended at the end of this file.
# EXP-173 isolate opening market sequence inspired by yhay81/shop-router-0911-simple (Apache-2.0).
# Kaggriculture EXP-167 candidate. Not submitted automatically.
# Attribution: thomastschinkel, yhay81, destbreso, aurax7, tetsutani,
# prvsiyan and Dmitrii Gluzdov. Apache-2.0 derivations; notices retained below.
# Kaggriculture v31 / EXP-157, Ahmed Berat Ozer, September 9 2026.
# Selected mechanism: crop_public_order. New independent confirmation is required.
# Public V221B/V224C production/timing lineage: prvsiyan, Apache-2.0.
# Original economics and integration; retained upstream licenses follow.
# Kaggriculture v28 / EXP-154, Ahmed Berat Ozer, September 9 2026.
# Changes: aurax7 day-end storage guard; Dmitrii Gluzdov physical terminal rescue
# adapted to v27, with 64 deterministic simulations. Apache-2.0.
# New action tapes and ordered shop-pair map: yhay81/shop-router-0909, Apache-2.0.
# Kaggriculture v25, EXP-149: Shop0908 production, sale lead, terminal cargo rescue.
# Runtime chassis: Apache-2.0; thomastschinkel, yhay81, tetsutani.
# Routing and public action data: yhay81/shop-router-0908, frozen September 8, 2026.
# 
#                                  Apache License
#                            Version 2.0, January 2004
#                         http://www.apache.org/licenses/
# 
#    TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
# 
#    1. Definitions.
# 
#       "License" shall mean the terms and conditions for use, reproduction,
#       and distribution as defined by Sections 1 through 9 of this document.
# 
#       "Licensor" shall mean the copyright owner or entity authorized by
#       the copyright owner that is granting the License.
# 
#       "Legal Entity" shall mean the union of the acting entity and all
#       other entities that control, are controlled by, or are under common
#       control with that entity. For the purposes of this definition,
#       "control" means (i) the power, direct or indirect, to cause the
#       direction or management of such entity, whether by contract or
#       otherwise, or (ii) ownership of fifty percent (50%) or more of the
#       outstanding shares, or (iii) beneficial ownership of such entity.
# 
#       "You" (or "Your") shall mean an individual or Legal Entity
#       exercising permissions granted by this License.
# 
#       "Source" form shall mean the preferred form for making modifications,
#       including but not limited to software source code, documentation
#       source, and configuration files.
# 
#       "Object" form shall mean any form resulting from mechanical
#       transformation or translation of a Source form, including but
#       not limited to compiled object code, generated documentation,
#       and conversions to other media types.
# 
#       "Work" shall mean the work of authorship, whether in Source or
#       Object form, made available under the License, as indicated by a
#       copyright notice that is included in or attached to the work
#       (an example is provided in the Appendix below).
# 
#       "Derivative Works" shall mean any work, whether in Source or Object
#       form, that is based on (or derived from) the Work and for which the
#       editorial revisions, annotations, elaborations, or other modifications
#       represent, as a whole, an original work of authorship. For the purposes
#       of this License, Derivative Works shall not include works that remain
#       separable from, or merely link (or bind by name) to the interfaces of,
#       the Work and Derivative Works thereof.
# 
#       "Contribution" shall mean any work of authorship, including
#       the original version of the Work and any modifications or additions
#       to that Work or Derivative Works thereof, that is intentionally
#       submitted to Licensor for inclusion in the Work by the copyright owner
#       or by an individual or Legal Entity authorized to submit on behalf of
#       the copyright owner. For the purposes of this definition, "submitted"
#       means any form of electronic, verbal, or written communication sent
#       to the Licensor or its representatives, including but not limited to
#       communication on electronic mailing lists, source code control systems,
#       and issue tracking systems that are managed by, or on behalf of, the
#       Licensor for the purpose of discussing and improving the Work, but
#       excluding communication that is conspicuously marked or otherwise
#       designated in writing by the copyright owner as "Not a Contribution."
# 
#       "Contributor" shall mean Licensor and any individual or Legal Entity
#       on behalf of whom a Contribution has been received by Licensor and
#       subsequently incorporated within the Work.
# 
#    2. Grant of Copyright License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       copyright license to reproduce, prepare Derivative Works of,
#       publicly display, publicly perform, sublicense, and distribute the
#       Work and such Derivative Works in Source or Object form.
# 
#    3. Grant of Patent License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       (except as stated in this section) patent license to make, have made,
#       use, offer to sell, sell, import, and otherwise transfer the Work,
#       where such license applies only to those patent claims licensable
#       by such Contributor that are necessarily infringed by their
#       Contribution(s) alone or by combination of their Contribution(s)
#       with the Work to which such Contribution(s) was submitted. If You
#       institute patent litigation against any entity (including a
#       cross-claim or counterclaim in a lawsuit) alleging that the Work
#       or a Contribution incorporated within the Work constitutes direct
#       or contributory patent infringement, then any patent licenses
#       granted to You under this License for that Work shall terminate
#       as of the date such litigation is filed.
# 
#    4. Redistribution. You may reproduce and distribute copies of the
#       Work or Derivative Works thereof in any medium, with or without
#       modifications, and in Source or Object form, provided that You
#       meet the following conditions:
# 
#       (a) You must give any other recipients of the Work or
#           Derivative Works a copy of this License; and
# 
#       (b) You must cause any modified files to carry prominent notices
#           stating that You changed the files; and
# 
#       (c) You must retain, in the Source form of any Derivative Works
#           that You distribute, all copyright, patent, trademark, and
#           attribution notices from the Source form of the Work,
#           excluding those notices that do not pertain to any part of
#           the Derivative Works; and
# 
#       (d) If the Work includes a "NOTICE" text file as part of its
#           distribution, then any Derivative Works that You distribute must
#           include a readable copy of the attribution notices contained
#           within such NOTICE file, excluding those notices that do not
#           pertain to any part of the Derivative Works, in at least one
#           of the following places: within a NOTICE text file distributed
#           as part of the Derivative Works; within the Source form or
#           documentation, if provided along with the Derivative Works; or,
#           within a display generated by the Derivative Works, if and
#           wherever such third-party notices normally appear. The contents
#           of the NOTICE file are for informational purposes only and
#           do not modify the License. You may add Your own attribution
#           notices within Derivative Works that You distribute, alongside
#           or as an addendum to the NOTICE text from the Work, provided
#           that such additional attribution notices cannot be construed
#           as modifying the License.
# 
#       You may add Your own copyright statement to Your modifications and
#       may provide additional or different license terms and conditions
#       for use, reproduction, or distribution of Your modifications, or
#       for any such Derivative Works as a whole, provided Your use,
#       reproduction, and distribution of the Work otherwise complies with
#       the conditions stated in this License.
# 
#    5. Submission of Contributions. Unless You explicitly state otherwise,
#       any Contribution intentionally submitted for inclusion in the Work
#       by You to the Licensor shall be under the terms and conditions of
#       this License, without any additional terms or conditions.
#       Notwithstanding the above, nothing herein shall supersede or modify
#       the terms of any separate license agreement you may have executed
#       with Licensor regarding such Contributions.
# 
#    6. Trademarks. This License does not grant permission to use the trade
#       names, trademarks, service marks, or product names of the Licensor,
#       except as required for reasonable and customary use in describing the
#       origin of the Work and reproducing the content of the NOTICE file.
# 
#    7. Disclaimer of Warranty. Unless required by applicable law or
#       agreed to in writing, Licensor provides the Work (and each
#       Contributor provides its Contributions) on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#       implied, including, without limitation, any warranties or conditions
#       of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
#       PARTICULAR PURPOSE. You are solely responsible for determining the
#       appropriateness of using or redistributing the Work and assume any
#       risks associated with Your exercise of permissions under this License.
# 
#    8. Limitation of Liability. In no event and under no legal theory,
#       whether in tort (including negligence), contract, or otherwise,
#       unless required by applicable law (such as deliberate and grossly
#       negligent acts) or agreed to in writing, shall any Contributor be
#       liable to You for damages, including any direct, indirect, special,
#       incidental, or consequential damages of any character arising as a
#       result of this License or out of the use or inability to use the
#       Work (including but not limited to damages for loss of goodwill,
#       work stoppage, computer failure or malfunction, or any and all
#       other commercial damages or losses), even if such Contributor
#       has been advised of the possibility of such damages.
# 
#    9. Accepting Warranty or Additional Liability. While redistributing
#       the Work or Derivative Works thereof, You may choose to offer,
#       and charge a fee for, acceptance of support, warranty, indemnity,
#       or other liability obligations and/or rights consistent with this
#       License. However, in accepting such obligations, You may act only
#       on Your own behalf and on Your sole responsibility, not on behalf
#       of any other Contributor, and only if You agree to indemnify,
#       defend, and hold each Contributor harmless for any liability
#       incurred by, or claims asserted against, such Contributor by reason
#       of your accepting any such warranty or additional liability.
# 
#    END OF TERMS AND CONDITIONS
# 
#    APPENDIX: How to apply the Apache License to your work.
# 
#       To apply the Apache License to your work, attach the following
#       boilerplate notice, with the fields enclosed by brackets "[]"
#       replaced with your own identifying information. (Don't include
#       the brackets!)  The text should be enclosed in the appropriate
#       comment syntax for the file format. We also recommend that a
#       file or class name and description of purpose be included on the
#       same "printed page" as the copyright notice for easier
#       identification within third-party archives.
# 
#    Copyright [yyyy] [name of copyright owner]
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""Kaggriculture route-replay chassis (pure Python, stdlib only).

A *route* is a pre-computed tape of 719 Kaggle-format actions
``{"farmer": [op, ...], "hands": [[op, ...], ...], "market": [[order, item, qty], ...]}``.
The chassis replays the tape chosen by a caller-supplied ``router`` and wraps it
in small reactive layers (each independently switchable via ``settings``):

    hand_align            pad/truncate hands to the real hand count      (fieldbook_logic)
    weed_repair           DIG a weed that blocks PLANT/BUILD, replay      (tetsutani + task spec)
    sell_lead             sell next step's lots one step early            (fieldbook _lead_sale)
    front_run             sell before the opponent's scheduled SELL       (hook; opponent_plan)
    budget_guard          fund each 72-step block's purchases             (six_day_budget_guard.hpp)
    room_guard            keep shed <= 99 at hour 23                      (tetsutani)
    clamp_sells           trim SELL orders to the projected shed          (tetsutani)
    dead_stock            sell stock the route will never sell            (tetsutani)
    terminal_liquidation  step >= 718: sell the whole projected shed      (fieldbook _terminal_sale)

Engine facts (verified against kaggle_environments 1.32.7, env_1_32_7.py):
  observation["farms"][p] = {"money", "tiles"[y][x], "farmer"[x,y], "hands"[[x,y]..],
                             "unlocked_quadrants", "hires_today"}
  tiles: None (empty) | "LOCKED" | {"kind": WEED|COOP|PASTURE|PLANT, "crop"/"animal", ...}
  observation["private"] = {"shed": {item: n}, "seeds": {crop: n}, "inventories": [{}...]}
  observation["market"] = {"inventory": {...}, "prices": {...}}
  observation["town"] = {"unlocked_shops": [...]}
  Agents act on steps 0..718 (interpreter marks DONE once step >= episodeSteps-2).
"""
from __future__ import annotations

import copy

PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
SEED_PRICE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
LAND_PRICES = (1000, 2000, 4000)
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
FRONT_RUN_ITEMS = ("MILK", "WOOL", "STRAWBERRY", "MELON")
LAST_ACT_STEP = 718
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

DEFAULT_SETTINGS = {
    "hand_align": True,
    "weed_repair": True,
    "sell_lead": True,
    "front_run": True,
    "budget_guard": True,
    "room_guard": True,
    "clamp_sells": True,
    "dead_stock": True,
    "terminal_liquidation": True,
    # tunables
    "block_turns": 72,
    "shed_capacity": 100,
    "board_size": 10,
    "max_orders": 10,
    "turns_per_day": 24,
    "min_sell_price": 2,
}


# --------------------------------------------------------------------------- helpers
def _get(value, key, default=None):
    """Field access that works for dicts and Kaggle Struct/attribute objects."""
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _step_of(observation):
    raw = _get(observation, "step")
    if raw is not None:
        return _int(raw)
    return _int(_get(observation, "day", 0)) * 24 + _int(_get(observation, "hour", 0))


def _shed_adjacent(pos, board):
    if not isinstance(pos, (list, tuple)) or len(pos) < 2:
        return False
    half = board // 2
    return pos[0] in (half - 1, half) and pos[1] in (half - 1, half)


def _tile_at(tiles, pos):
    try:
        x, y = int(pos[0]), int(pos[1])
        return tiles[y][x]
    except (TypeError, ValueError, IndexError):
        return "LOCKED"


def _is_noop(act, tile, inv, seeds, pos, board):
    """True when the engine will certainly ignore ``act`` (mirrors _apply_unit_action)."""
    if not act:
        return True
    op = act[0]
    x, y = pos[0], pos[1]
    if op in MOVES:
        dx, dy = MOVES[op]
        return not (0 <= x + dx < board and 0 <= y + dy < board)
    if op == "PASS":
        return True
    adjacent = _shed_adjacent(pos, board)
    if op == "DROP":
        return (not adjacent) or (not inv)
    if op == "PICKUP":
        return not adjacent
    if op == "PLACE":
        item = act[1] if len(act) > 1 else None
        if item in ANIMAL_STRUCTURE and isinstance(tile, dict) \
                and _get(tile, "kind") == ANIMAL_STRUCTURE[item] and _get(tile, "animal") is None:
            return _int(_get(inv, item, 0)) <= 0
        return (not adjacent) or _int(_get(inv, item, 0)) <= 0
    if tile == "LOCKED":
        return True
    is_dict = isinstance(tile, dict)
    kind = _get(tile, "kind") if is_dict else None
    animal = is_dict and _get(tile, "animal") is not None
    if op == "PLANT":
        return tile is not None or _int(_get(seeds, act[1] if len(act) > 1 else None, 0)) <= 0
    if op == "WATER":
        return kind != "PLANT" or bool(_get(tile, "watered_today"))
    if op == "HARVEST":
        return (not is_dict) or _int(_get(tile, "yield_units", 0)) <= 0
    if op == "FERTILIZE":
        return kind != "PLANT" or _int(_get(inv, "FERTILIZER", 0)) <= 0
    if op == "DIG":
        return tile is None or animal
    if op in ("BUILD_COOP", "BUILD_PASTURE"):
        return tile is not None
    if op == "FEED":
        return (not animal) or bool(_get(tile, "fed_today")) or _int(_get(inv, "WHEAT", 0)) <= 0
    if op == "COLLECT_FERTILIZER":
        return (not animal) or (not _get(tile, "fertilizer_available"))
    if op == "CARE":
        return (not animal) or bool(_get(tile, "cared_today"))
    return True


class _View:
    """Cheap per-step snapshot of everything the layers read from the observation."""

    def __init__(self, observation, player, cfg):
        farms = list(_get(observation, "farms", []) or [])
        self.farm = farms[player] if player < len(farms) else {}
        self.rival = farms[1 - player] if len(farms) >= 2 and 1 - player < len(farms) else {}
        private = _get(observation, "private", {}) or {}
        self.shed = {k: max(0, _int(v)) for k, v in dict(_get(private, "shed", {}) or {}).items()}
        self.seeds = dict(_get(private, "seeds", {}) or {})
        self.invs = [dict(i or {}) for i in (_get(private, "inventories", []) or [])]
        market = _get(observation, "market", {}) or {}
        self.prices = {k: _int(v) for k, v in dict(_get(market, "prices", {}) or {}).items()}
        self.money = float(_get(self.farm, "money", 0.0) or 0.0)
        self.tiles = _get(self.farm, "tiles", []) or []
        self.board = len(self.tiles) or cfg["board_size"]
        self.positions = [_get(self.farm, "farmer", None)] + [list(p) for p in (_get(self.farm, "hands", []) or [])]
        self.hires_today = _int(_get(self.farm, "hires_today", 0))
        self.quadrants = len(list(_get(self.farm, "unlocked_quadrants", []) or []))

    def inv(self, idx):
        return self.invs[idx] if idx < len(self.invs) else {}

    def in_hands(self, item):
        return sum(max(0, _int(_get(inv, item, 0))) for inv in self.invs)


# --------------------------------------------------------------------------- chassis
class Chassis:
    """Replays ``routes[router(...)]`` with reactive safety/market layers.

    routes         : {route_id: list of >= 719 Kaggle action dicts}
    router         : callable(observation, step, state_dict) -> route_id, called every
                     step; ``state_dict`` is per-player and persists across the game.
    settings       : overrides for DEFAULT_SETTINGS (layer switches + tunables)
    opponent_plan  : optional list of the opponent's expected actions (front_run hook)
    """

    def __init__(self, routes, router=None, settings=None, opponent_plan=None):
        self.routes = {rid: list(tape) for rid, tape in routes.items()}
        self.router = router or (lambda observation, step, state: next(iter(self.routes)))
        self.cfg = dict(DEFAULT_SETTINGS)
        self.cfg.update(settings or {})
        self.opponent_plan = opponent_plan
        self.players = {}
        self.diagnostics = {"layer_fallbacks": 0, "entry_fallbacks": 0}
        self._future_sells = {}   # route id -> {item: [remaining planned SELL qty from step t]}

    # ---- state -----------------------------------------------------------------
    def _state(self, player, step):
        st = self.players.get(player)
        if st is None or step == 0 or step <= st["last_step"]:
            st = {"last_step": -1, "route": None, "router_state": {},
                  "pending": {}, "sell_state": {"due_step": -1, "suppress": {}}}
            self.players[player] = st
        st["last_step"] = step
        return st

    def _route_action(self, route, step):
        tape = self.routes[route]
        if 0 <= step < len(tape) and isinstance(tape[step], dict):
            return copy.deepcopy(tape[step])
        return copy.deepcopy(PASS_ACTION)

    def future_sells(self, route, item, step):
        """Planned SELL quantity of ``item`` in route steps >= ``step`` (suffix sums)."""
        table = self._future_sells.get(route)
        if table is None:
            tape = self.routes[route]
            n = len(tape)
            table = {p: [0] * (n + 1) for p in PRODUCTS}
            for t in range(n - 1, -1, -1):
                for p in PRODUCTS:
                    table[p][t] = table[p][t + 1]
                for o in (tape[t].get("market") or []) if isinstance(tape[t], dict) else []:
                    if o and o[0] == "SELL" and len(o) >= 3 and o[1] in table:
                        table[o[1]][t] += max(0, _int(o[2]))
            self._future_sells[route] = table
        col = table.get(item)
        return col[step] if col and 0 <= step < len(col) else 0

    # ---- main entry -----------------------------------------------------------
    def act(self, observation, configuration=None):
        if len(_get(observation, "farms", []) or []) < 2:
            raise ValueError("incomplete observation")  # factory falls back to tape
        step = _step_of(observation)
        player = _int(_get(observation, "player", 0))
        st = self._state(player, step)
        cfg = self.cfg
        view = _View(observation, player, cfg)

        route = self.router(observation, step, st["router_state"])
        if route not in self.routes:
            route = st["route"] if st["route"] in self.routes else next(iter(self.routes))
        st["route"] = route
        action = self._route_action(route, step)
        raw = copy.deepcopy(action)
        try:
            if cfg["hand_align"]:
                self._hand_align(action, view)
            if cfg["weed_repair"]:
                self._weed_repair(action, view, st, route, step)
            if cfg["sell_lead"] or cfg["front_run"]:
                self._apply_suppression(action, st["sell_state"], step)
            projected = self._projected_shed(action, view)
            lead_available = dict(projected)
            next_sup = {"due_step": -1, "suppress": {}, "r36_debts": st["sell_state"].get("r36_debts", {})}
            if cfg["sell_lead"]:
                self._sell_lead(action, view, lead_available, route, step, next_sup)
            if cfg["front_run"] and self.opponent_plan:
                self._front_run(action, view, lead_available, route, step, next_sup)
            st["sell_state"] = next_sup
            if cfg["budget_guard"]:
                self._budget_guard(action, view, route, step)
            if cfg["room_guard"]:
                self._room_guard(action, view, route, step)
            if cfg["clamp_sells"]:
                self._clamp_sells(action, projected)
            if cfg["dead_stock"]:
                self._dead_stock(action, view, projected, route, step)
            if cfg["terminal_liquidation"]:
                self._terminal_liquidation(action, projected, step)
            action["market"] = action["market"][: cfg["max_orders"]]
            return action
        except Exception:
            self.diagnostics["layer_fallbacks"] += 1
            return raw

    # ---- layer: hand_align ----------------------------------------------------
    def _hand_align(self, action, view):
        """Pad with PASS / truncate the tape's hand list to the real number of hands
        (fieldbook_logic.act). Extra hands would be ignored by the engine anyway;
        missing ones just idle, so alignment only tidies the action."""
        expected = max(0, len(view.positions) - 1)
        hands = list(action.get("hands") or [])
        hands.extend([["PASS"] for _ in range(max(0, expected - len(hands)))])
        action["hands"] = hands[:expected]

    # ---- layer: weed_repair ---------------------------------------------------
    def _weed_repair(self, action, view, st, route, step):
        """If a PLANT/BUILD_* target tile is a WEED, DIG now and queue the intended
        action for that unit; the queue replays on a later step when the unit still
        stands there and its tape action would be a no-op (the displaced no-op is
        queued behind it, so PLANT -> WATER chains survive). A PLANT is only replayed
        when the unit's next tape action is not a move, so the mandatory same-day
        WATER can follow; otherwise the seed is kept. A no-op turn spent on a weed
        is also converted to DIG (tetsutani weed_dig)."""
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        pending = st["pending"]
        tape = self.routes[route]
        nxt = tape[step + 1] if step + 1 < len(tape) and isinstance(tape[step + 1], dict) else {}
        next_units = [nxt.get("farmer") or ["PASS"]] + list(nxt.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            pos = view.positions[i]
            if not isinstance(pos, (list, tuple)):
                continue
            pos = (int(pos[0]), int(pos[1]))
            tile = _tile_at(view.tiles, pos)
            act = list(units[i])
            queue = pending.get(i)
            if queue and queue[0][0] != pos:
                pending.pop(i, None)
                queue = None
            is_weed = isinstance(tile, dict) and _get(tile, "kind") == "WEED"
            noop = _is_noop(act, tile, view.inv(i), view.seeds, pos, view.board)
            next_op = next_units[i][0] if i < len(next_units) and next_units[i] else "PASS"
            if act and act[0] in ("PLANT", "BUILD_COOP", "BUILD_PASTURE") and is_weed:
                pending.setdefault(i, []).append((pos, act))
                act = ["DIG"]
            elif queue and noop:
                _, replay = queue[0]
                if replay[0] == "PLANT" and next_op in MOVES:
                    pending.pop(i, None)          # WATER could never follow: keep the seed
                else:
                    queue.pop(0)
                    if act and act[0] != "PASS" and act[0] not in MOVES:
                        queue.append((pos, act))
                    act = replay
                    if not queue:
                        pending.pop(i, None)
            elif is_weed and noop:
                act = ["DIG"]
            units[i] = act
        action["farmer"] = units[0]
        action["hands"] = units[1:]

    # ---- projected shed -------------------------------------------------------
    def _projected_shed(self, action, view):
        """Shed contents after this step's unit actions but before the market runs:
        PICKUP removes, DROP/PLACE(non-animal) near the shed adds up to capacity
        (fieldbook _projected_shed / tetsutani projected shed)."""
        cap = self.cfg["shed_capacity"]
        proj = {p: view.shed.get(p, 0) for p in PRODUCTS}
        for k, v in view.shed.items():
            proj.setdefault(k, v)
        total = sum(proj.values())
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            if not _shed_adjacent(view.positions[i], view.board):
                continue
            act = units[i]
            op = act[0] if act else "PASS"
            inv = view.inv(i)
            if op == "PICKUP" and len(act) >= 2 and act[1] in proj:
                qty = min(proj[act[1]], max(0, _int(act[2]) if len(act) >= 3 else 1))
                proj[act[1]] -= qty
                total -= qty
            elif op == "DROP":
                for item, held in inv.items():
                    take = min(max(0, _int(held)), max(0, cap - total))
                    if take > 0:
                        proj[item] = proj.get(item, 0) + take
                        total += take
            elif op == "PLACE" and len(act) >= 2 and act[1] not in ANIMAL_STRUCTURE:
                item = act[1]
                take = min(max(0, _int(act[2]) if len(act) >= 3 else 1),
                           max(0, _int(_get(inv, item, 0))), max(0, cap - total))
                if take > 0:
                    proj[item] = proj.get(item, 0) + take
                    total += take
        return proj

    # ---- layer: sell_lead / front_run suppression ------------------------------
    @staticmethod
    def _apply_suppression(action, sell_state, step):
        """Remove from this step's SELLs the quantities already sold a step early."""
        if sell_state.get("due_step") != step:
            return
        remaining = dict(sell_state.get("suppress", {}))
        kept = []
        for order in action.get("market") or []:
            order = list(order)
            if order and order[0] == "SELL" and len(order) >= 3 and remaining.get(order[1], 0) > 0:
                removed = min(max(0, _int(order[2])), remaining[order[1]])
                order[2] = _int(order[2]) - removed
                remaining[order[1]] -= removed
                # A zero-quantity order keeps later market race slots intact.
            kept.append(order)
        action["market"] = kept

    @staticmethod
    def _add_sell(action, item, qty, max_orders, merge=True):
        market = action.setdefault("market", [])
        if merge:
            for order in market:
                if order and order[0] == "SELL" and order[1] == item:
                    order[2] = _int(order[2]) + qty
                    return True
        if len(market) >= max_orders:
            return False
        market.append(["SELL", item, qty])
        return True

    def _sell_lead(self, action, view, projected, route, step, next_sup):
        """fieldbook _lead_sale: when step % 4 != 0 (no town consumption between the
        two steps) sell the lots the tape plans to SELL next step now, for products
        other than WHEAT/FERTILIZER we already hold, and suppress them next step.
        Skipped at the last step, at shop-unlock boundaries and if a SELL for that
        product is already queued this step."""
        cfg = self.cfg
        nxt = step + 1
        unlock_period = 3 * cfg["turns_per_day"]
        if nxt > LAST_ACT_STEP or nxt % unlock_period == 0 or step % 4 == 0:
            return
        tape = self.routes[route]
        future = tape[nxt] if nxt < len(tape) and isinstance(tape[nxt], dict) else {}
        planned = {}
        for o in future.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3 and o[1] in PRODUCTS:
                planned[o[1]] = planned.get(o[1], 0) + max(0, _int(o[2]))
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for item in PRODUCTS:
            if item in ("WHEAT", "FERTILIZER") or planned.get(item, 0) <= 0 or item in already:
                continue
            qty = min(projected.get(item, 0), planned[item])
            if qty <= 0 or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    def _front_run(self, action, view, projected, route, step, next_sup):
        """Hook: if ``opponent_plan`` (their expected tape) schedules a SELL of
        MILK/WOOL/STRAWBERRY/MELON next step, sell what we hold of it now (before
        their supply depresses the price) and suppress our own SELL of that quantity
        next step. Bounded by our own remaining planned sales so it never dumps."""
        cfg = self.cfg
        nxt = step + 1
        plan = self.opponent_plan
        if nxt > LAST_ACT_STEP or nxt >= len(plan) or not isinstance(plan[nxt], dict):
            return
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for o in plan[nxt].get("market") or []:
            if not (o and o[0] == "SELL" and len(o) >= 3 and o[1] in FRONT_RUN_ITEMS):
                continue
            item = o[1]
            if item in already or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            own_next = sum(max(0, _int(x[2])) for x in self.routes[route][nxt].get("market", [])
                           if len(x) >= 3 and x[0] == "SELL" and x[1] == item)
            qty = min(projected.get(item, 0), max(0, _int(o[2])), own_next)
            if qty <= 0:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            already.add(item)
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    # ---- layer: budget_guard --------------------------------------------------
    def _block_requirements(self, view, route, start, end):
        """Planned purchase cost and item reserves for tape steps [start, end)
        (six_day_budget_guard.hpp calculate_six_day_requirements)."""
        tape = self.routes[route]
        budget = 0.0
        seed_bal, item_bal = {}, {}
        seed_need, item_need = {}, {}
        hires_by_day = {}
        quadrants = view.quadrants
        for t in range(start, min(end, len(tape))):
            a = tape[t] if isinstance(tape[t], dict) else {}
            for u in [a.get("farmer") or ["PASS"]] + list(a.get("hands") or []):
                if not u:
                    continue
                op = u[0]
                arg = u[1] if len(u) > 1 else None
                qty = max(1, _int(u[2]) if len(u) > 2 else 1)
                if op == "PLANT" and arg in SEED_PRICE:
                    seed_bal[arg] = seed_bal.get(arg, 0) - 1
                    seed_need[arg] = max(seed_need.get(arg, 0), -seed_bal[arg])
                elif op == "FEED":
                    item_bal["WHEAT"] = item_bal.get("WHEAT", 0) - 1
                    item_need["WHEAT"] = max(item_need.get("WHEAT", 0), -item_bal["WHEAT"])
                elif op == "FERTILIZE":
                    item_bal["FERTILIZER"] = item_bal.get("FERTILIZER", 0) - 1
                    item_need["FERTILIZER"] = max(item_need.get("FERTILIZER", 0), -item_bal["FERTILIZER"])
                elif op == "PLACE" and arg is not None:
                    item_bal[arg] = item_bal.get(arg, 0) - qty
                    item_need[arg] = max(item_need.get(arg, 0), -item_bal[arg])
            for o in a.get("market") or []:
                if not o:
                    continue
                op = o[0]
                item = o[1] if len(o) > 1 else None
                qty = max(1, _int(o[2]) if len(o) > 2 else 1)
                if op == "HIRE":
                    day = (t - start) // self.cfg["turns_per_day"]
                    hires_by_day[day] = hires_by_day.get(day, 0) + 1
                elif op == "BUY_LAND":
                    extra = quadrants - 1
                    if 0 <= extra < len(LAND_PRICES):
                        budget += LAND_PRICES[extra]
                        quadrants += 1
                elif op == "BUY_SEED" and item in SEED_PRICE:
                    budget += SEED_PRICE[item] * qty
                    seed_bal[item] = seed_bal.get(item, 0) + qty
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    budget += view.prices.get(item, 0) * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
                elif op == "BUY_ANIMAL" and item in ANIMAL_COST:
                    budget += ANIMAL_COST[item] * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
        for day, n in hires_by_day.items():
            first = view.hires_today if day == 0 else 0
            for k in range(n):
                budget += _fib(first + k)
        return budget, item_need

    def _budget_guard(self, action, view, route, step):
        """At every block boundary (step % 72 == 0) make sure cash + the value of
        stock the block already plans to sell covers the block's purchases (hires,
        land, seeds, animals, products). A shortfall is covered by extra SELLs of
        unprotected shed stock, highest price first; SELLs are moved in front of
        the buys so the money is there when they execute."""
        cfg = self.cfg
        block = cfg["block_turns"]
        if block <= 0 or step % block != 0:
            return
        budget, item_need = self._block_requirements(view, route, step, step + block)
        market = action.setdefault("market", [])
        existing = {}
        for o in market:
            if o and o[0] == "SELL" and len(o) >= 3:
                existing[o[1]] = existing.get(o[1], 0) + max(0, _int(o[2]))
        cash = view.money
        for item in PRODUCTS:
            planned = max(existing.get(item, 0), self.future_sells(route, item, step)
                          - self.future_sells(route, item, step + block))
            cash += min(view.shed.get(item, 0), planned) * view.prices.get(item, 0)
        shortfall = budget - cash
        if shortfall <= 0:
            return
        candidates = []
        for item in PRODUCTS:
            price = view.prices.get(item, 0)
            if price < cfg["min_sell_price"]:
                continue
            protected = max(0, item_need.get(item, 0) - view.in_hands(item))
            avail = view.shed.get(item, 0) - protected - existing.get(item, 0)
            if avail > 0:
                candidates.append((-price, item, avail, price))
        candidates.sort()
        added = False
        for _, item, avail, price in candidates:
            if shortfall <= 0:
                break
            qty = min(avail, -(-int(shortfall) // price))
            if self._add_sell(action, item, qty, cfg["max_orders"]):
                shortfall -= qty * price
                added = True
        if added:
            sells = [o for o in market if o and o[0] == "SELL"]
            others = [o for o in market if not (o and o[0] == "SELL")]
            action["market"] = sells + others

    # ---- layer: room_guard ----------------------------------------------------
    def _room_guard(self, action, view, route, step):
        """tetsutani room_guard: at hour 23 the end-of-day drop pushes every unit's
        inventory into the shed and overflow is destroyed. Estimate the shed after
        this step (stock + carried + harvest/collect - feed/fertilize/place + buys -
        sells) and, if it exceeds capacity-1, add SELLs preferring products with no
        future planned sale, then highest price."""
        cfg = self.cfg
        if step % cfg["turns_per_day"] != cfg["turns_per_day"] - 1:
            return
        cap = cfg["shed_capacity"]
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        carried = sum(max(0, _int(n)) for inv in view.invs for n in inv.values())
        produced = consumed = 0
        for i in range(min(len(units), len(view.positions))):
            tile = _tile_at(view.tiles, view.positions[i])
            a = units[i]
            if not a:
                continue
            op = a[0]
            if op == "HARVEST" and isinstance(tile, dict):
                produced += max(0, _int(_get(tile, "yield_units", 0)))
            elif op == "COLLECT_FERTILIZER" and isinstance(tile, dict) and _get(tile, "fertilizer_available"):
                produced += 1
            elif op in ("FEED", "FERTILIZE"):
                consumed += 1
            elif op == "PLACE" and len(a) > 1 and a[1] in ANIMAL_STRUCTURE:
                consumed += 1
        market = action.setdefault("market", [])
        planned_sells, planned_buys = {}, 0
        for o in market:
            if not o:
                continue
            if o[0] == "SELL" and len(o) >= 3:
                planned_sells[o[1]] = planned_sells.get(o[1], 0) + max(0, _int(o[2]))
            elif o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                planned_buys += max(0, _int(o[2]))
        shed_total = sum(view.shed.values())
        fillable = sum(min(view.shed.get(it, 0), n) for it, n in planned_sells.items())
        needed = shed_total + carried + produced - consumed + planned_buys - fillable - (cap - 1)
        if needed <= 0:
            return
        priority = sorted(PRODUCTS, key=lambda it: (self.future_sells(route, it, step + 1) > 0,
                                                   -view.prices.get(it, 0), it))
        for item in priority:
            avail = max(0, view.shed.get(item, 0) - planned_sells.get(item, 0))
            qty = min(needed, avail)
            if qty <= 0 or view.prices.get(item, 0) < 1:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"]):
                continue
            planned_sells[item] = planned_sells.get(item, 0) + qty
            needed -= qty
            if needed <= 0:
                break

    # ---- layer: clamp_sells ---------------------------------------------------
    @staticmethod
    def _clamp_sells(action, projected):
        """Clamp against a sequential stock upper bound, retaining market slots.

        Earlier BUY_PRODUCT orders can fund a wheat wash's sell leg. Their full
        quantity is an upper bound; the engine enforces actual cash/capacity.
        Removing empty orders would change the later lockstep market races.
        """
        avail = dict(projected)
        kept = []
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                have = avail.get(o[1], 0)
                n = min(_int(o[2]), have)
                n = max(0, n)
                avail[o[1]] = have - n
                kept.append(["SELL", o[1], n])
            else:
                kept.append(o)
                if o and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                    avail[o[1]] = avail.get(o[1], 0) + max(0, _int(o[2]))
        action["market"] = kept

    # ---- layer: dead_stock ----------------------------------------------------
    def _dead_stock(self, action, view, projected, route, step):
        """tetsutani dead_stock: stock beyond everything the rest of the route still
        plans to SELL is dead; sell it now when price > 1 (on day 29 everything not
        already in this step's orders is dead). Highest value lots first."""
        planned = {}
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                planned[o[1]] = planned.get(o[1], 0) + _int(o[2])
        day = step // self.cfg["turns_per_day"]
        extra = []
        for item in PRODUCTS:
            have = projected.get(item, 0) - planned.get(item, 0)
            if have <= 0:
                continue
            surplus = have if day >= 29 else have - self.future_sells(route, item, step + 1)
            if surplus > 0 and view.prices.get(item, 0) > 1:
                extra.append(["SELL", item, surplus])
        extra.sort(key=lambda o: -view.prices.get(o[1], 0) * o[2])
        action["market"] = (action.get("market") or []) + extra

    # ---- layer: terminal_liquidation -----------------------------------------
    def _terminal_liquidation(self, action, projected, step):
        """fieldbook _terminal_sale: on the final acting step (>= 718) replace the
        market orders with a SELL of the whole projected shed."""
        if step < LAST_ACT_STEP:
            return
        action["market"] = [["SELL", item, qty] for item, qty in projected.items()
                            if qty > 0 and item in PRODUCTS][: self.cfg["max_orders"]]


# --------------------------------------------------------------------------- factory
def make_agent(routes, router=None, opponent_plan=None, **settings):
    """Build a Kaggle ``agent(observation, configuration)`` closure that never raises:
    a failure inside a layer falls back to the raw tape action, and a failure even
    before that falls back to PASS (with hands padded when possible)."""
    chassis = Chassis(routes, router, settings, opponent_plan)

    def agent(observation, configuration=None):
        try:
            return chassis.act(observation, configuration)
        except Exception:
            chassis.diagnostics["entry_fallbacks"] += 1
            try:
                step = _step_of(observation)
                player = _int(_get(observation, "player", 0))
                tape = chassis.routes.get(chassis.players.get(player, {}).get("route"),
                                          next(iter(chassis.routes.values())))
                if 0 <= step < len(tape):
                    return copy.deepcopy(tape[step])
            except Exception:
                pass
            try:
                farms = _get(observation, "farms", []) or []
                hands = _get(farms[_int(_get(observation, "player", 0))], "hands", []) or []
                return {"farmer": ["PASS"], "hands": [["PASS"] for _ in hands], "market": []}
            except Exception:
                return copy.deepcopy(PASS_ACTION)

    agent.chassis = chassis
    return agent

# Extracted from the frozen One More Wheat source on 2026-09-22.
# Upstream Apache-2.0 notices are retained above. Generic library only.


# Public actions only; no hidden-state or rival-identity input.
import base64,json,zlib
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rM%U2hyoa{MoR=EHJ^;%fcIlje4X(=G*l+~B+*77O?c1IGDb?Ki{!-4e;^>FJD&h|I2`cI_t-9BR6&Dyu3pGBWb#|GxOwUw`|@-+#OKr=Kt0-G2CRaesO7Z@>P>zx?OtUwr=YAHV+g?|=WV&p-cs@uyFJ`{nkhH$UFKy|}!1b+^B`yt==9{Pnx{cdtLa`uO?x`yY0<pZ|Sv_+<JIAAZ>F-hKHm_y2Qw^2|4{{_^SF>>HD(f7rc!d;I=~C;#x~{q92iKwetD+MhnXdHed8&y(`;)5Et-Z#H}D>Hl7;UmhPG|BerJIb&~cU+vI@{e1D$-TRL}Jd7LtwBLRBcyTYM6)tGLZcl%(J$aGGM_tZ-;IC0LmE-)*9=TjC^c(gPi-#TlbiU|M6MwS2=y#9XX!?#gR4~2v#6QjG?7d#yJ`HdBVVd>NulLiJFZ*%#_U<S2CLeaY*VE^ho5B|OaQEqCF5!f)eSVx?v<c^vI3N1SHu?O~?Z@4Fy6AuY@;1qiS_}o)Hu>VGm6?6<)1#)hf=^gGeTOxI13K=}=?%aPojhmS>#OE1oK5O^VGrzXmwVvwl*j*p=k@s6;y2~zzkYxB?)3S`r_Cm~I<LlF@7g0g>BU78pMKU^-h$14@{Q-8?x$}+7g-$M@&GJ94qq|PXvTk-34Z#C9I)V|o2}3E;+3y_b@%q|?$yU%{=9qt@y**e|9tx9r(@4NP<d_;kFDmMO!K&K0^lJq8xnCnHsq7iTp`ayI$-qfTDUyqYYuL}V#v^aLW6LYW9f)&PQM?2?b98GhLEh2ymXJ&os1g4OwG_{4?+Id<FI_I6CO+)WID8?b%4F?8uBs(hKswnhQaHs+I8}krcHEoBHg_%zkB-1DT<Lh70lV;|1N&0`~R)4KF61U<7nE!Gi#9VLXQe)YsVW>eK~O07NMx~Eyyi7wFT!}z{Z{CI>tFGmT=}Et@xJNsn)Or@HJ!oizfOt!W#hyP60-VCK;ijqw7L1;1$Q5?Vg}90-!?<I|iu0cL`91bz6HLiS&AA?}HzLB7oph*Ovkq#PlF=prU89@D|>&O8~eKWuqWMUH%r-^uz7@zmlmiyqpwc9X2t<^8m1R2oC|qRJWJ7lfbthC)1o3d0D}41dxk0QV9kgtt>*Q`6CPf?Ze0SxBEZs-oO8wHMKE-I4<wBIp<Roz=2}Wy12V97q5`c_Vf;=MO|L<mk@@H5Zi1PYwpD~XVdeh-+1V&d;%B}I<gkeFFoSPO_+Vj^c!?eH=dBW<9G-J6kqeC^x0>8z;5JJ1>e&eg6GZBhy4F=bq!Gc=Kc@q{W6zgjPsieO^(?1f>yc0$1ws26rIz%7Q{vGVhXe!FAZ=>f$O+#A|%@#hLnCVf0JZssT1G9A;2UpuXH&Z8`B*|F9h7+0L~rXaT#a!{5F<FiClnmxhl5=j#k2H5&fO%HK50~e%~M$O`L7VnF&r{(cuFN0VojhDXFK{vj=pA2lqWi0_SgL01Lq*Vc$2#rvgs^W`6j{2@ODC8~sf1*x-W>j11W0I<tm6=lq8uUOVs?$39@JFU?-Jvj#K=jebgJumGqsfAr-T=NT~063B3uyHAz$wsKf=y!199`W0UQfKINv?tMN22a7mz@UDs;mys)Pd+cdMQA!>hljdUf4J5Vf9ya~>^aTJG6n?0<P1Ri#Feym&S*+U#%LNyPU@otMF_Z=HWJk{@(_1MX{(KH>nuv+*r@VX4S?73v1FTrNxxy^YqtFu+e|pJB_q4aJ)+@lEB>god0u6mHn4wu@-^d<g^$>}_H~-<d+2aEEB@X0C-l64lCOEQs8s_uC&=55~4<scD%LJm*_=w4Qh=GV6P$?7uQ?`m?5oc)`z7Bgrj4}%}5mq4Mkw+VjIq@WX{5B@eq_@?`xyCGLCFeadoKOT%6QOU?L4fx~z1#-LuRsQgJ}F0XN0^bZ?#oML2*RB+SvOe>)qXrnMk8+z&B?~)o4QUzZwqF)k`YLCBb4-nU-58u0~|wZXRv+O9~gMyIh;yLoQdk(Ih8?%W07%y0|ok~l6g5^uPf&>Zqb~hQTpPz%@&>z0|iTd7$9#q-j`IEW<=oL*Tydy^ST9O`iyXHCAHag2n$v4VV8Y-UrO@9I}(<FjG$KNwZJsA5^uTW6-NpQ@Z63YkRMO%O*rJYzq@-2PDoykKM}UFDlz-zNO{lU&7SP-bJY9#!Z^qir*N9dnAeve@N|d_^j&q%A*O!kIe3cv#02`|iaGO~s9QAszX<bXPCH>f#G2K`z;nv?2wx;lYtB=w61#OowsK8!%R|U(v^mOUz{3Vh>Bl*2Xsb*y0*I)DLRnh;7PPZY*6jPcyAQkS>x)PRfS~FWL$D^Y)WhOUuU%fWtXdoMN*0{#$k)zRKz$x}-;#VjbfeizW~7hMrcx*0(h|%N{&Ee!|2U?&<(Y|6!<$e2m(%FgU3zs{6~LG4vTPek^Uc#UDdEvPNrTNKn{veJ=IR{!J^h;+7=u~iy&ZKmu!=DcMg;?p2U%$sYPa_I8o4UcVy>ly(ksE$3Tn_7*ls~y2?Pu6(|@G6NG|+w$>9fcErw{mghZyc4@RI!6=Ul9FpM%slxoDZgHJWV1FWtk@S@hfQpVz^^s@VI2%uAd>v&#6d7eG2#?Je=d5?rFRZ0Q+nT{!d%8FJ3zzyDLOybUVQBkT2BpDis%x(;>P@UY_Vq}$BB}GlghG6^YX1P+cI3O)puuD0kY~oZAh>?`pma}&V0?l)-+Y)SAP6%)A3psghopiP()}SXhz8!~_@h=&(uw2i!tw&#gkIiP#F1z&Rkm)*rIQAs3!N_G4UT##I9fL&aD@M*!4C&|i6`xy4B?DJ^phU$tL4H{{!+ZHs00FWvydu-(XDb(~TbD{Ngeeq_aRg>28S*->-+XUO&x+(NxEbd_P-9Yhu78lz!5bmEZ5>4{W&?d|&;tidL`GKWkT2P>$<LF>4j8q{JdWh9qI@#Qdp~0|XQ$^6X8q%vw|{xa|Jf0rk}!0gE*2k5Z<R!;Esab^&mN{vE3qL2QbiFH6vL_4h&8CVfNKB>%_-A?IDYabmK51|K4GPEF~R53x&W_roU4f@5pU5HOIDlVNQGd$2q<VS_y!WFQ0$0!6Sm{n0eW*<u)xbuQP9&Wn9BTdwi)H{pnFaWJ?iknCQIyk`CfasN9PB4BQf({0H)<yfa&C7i@+1g>F7DKP4(=0Idw@_N;ky9%|>n-u7FdejYY#jgUTgAkb4fUu(%8{CsW?ze0(48e!Ts7mv#brn&^VGH#o5ZCyXahx^@;P87&StNIAqRLjc>dDr)aX`XXtD;D!k0q?l<VbZ7HCT{QZqr|^9CsQVxt66+7KBVZ5Lq2JiS+px7UQ^V;2lb9DHmmF5Gyhs%TL+Wfyg%z0Bszaw}N7G}unky;1qQ&OT;@FUOhqD7dq%C2{$%9OzqLqr=-}H{>rrWPk$QVCkYZt~>C~W$9aT^lhz|Pf{eN-!ah@QA;A>bn$<Qscc5;1VaB8G$&@AWc#;KyG#D<tCUnsvDXEkL3Zix(bTIH5l0J_$INGkuD@`zQEhK%qrkq9btQ3scpzc#Cxs0xP7r;%PFjA!XD}`~&{2xsE2bRxZ~?K%ZM!?YhdDc1u~}AEl<_j7~#hy+rva#<h1!D1HkXCPF;S$t{v<qJ{Gun5zkUDe`;L$!i!YI2D-`Kc7dz4L$nFrvFT|-zd@rIJ!Hps04;>=M0s*rF?0Ci7bdhlEFP#5xMzsQKNjp(RiVuOj)FB^+4nCi;!<7K2GuRGL>odfRF{J&6j73K#?BiKJq%rRx4RwLXqnruu<BgYpO*lgbq?7rp$%X(@*HIwdxPt`Pz|+D>SWMJ!;uD_!eZRj7&Fo+quGxZ=qiN$S@@0s>~F#^q|+4c3-8c+?*Yj+54Ex*2ZME6olCNr2uv6&DHk4!3N|6T|N>O<H2vjJ*p~bO|6qas`4g5adp*btLMmHx4#G^(>(oc>fKLZLj>Xo8Dv{&Y{ry<0o5}`G0-$tcN~td%&|!LIx-4mDSKNP&o70J=FMKf)fUPBU@{-Z>NpUH3g~Kv_RY;%<*QBm0YN9T|Hr~^E(}9DBwz|dX4Tj&nFbb>a45W483M5};DUD4Y@)PU<Phv^=}1TPq8`#xUd}Z8ApDD9E^tEUwm@A|y15=#^J-1z6}m9s-~h=3G<F{ugT_7W@nH~6#(2TwR+bBlJ@f?<`S((u8Yl`DAsJ}C&>dqOA9)$DqbebBQ43$O;-umX;1M==4&uxZs?5^s5yLtsFC=1w*g_d=Kpp9xb-M}!{X-0xuEl{s?@gOX)QK|ZVJ*$h;JI7Gl`H7kOErMb$Eab3%i#|Cnv@EI!cIHWQD{9ZTW+T(jI#vZS<}WT5mk=tA4<<vFU=Iv)-y<fi7|~4WGTcwHJF)~Oz39-c4(H5(P9H)t0Q$pPCQl=sc+6zh2}tEkk?SCQg{CQwW~t9`~G{Ei6#^7M=DLAE&&b`FccsCWceLkrXd;_kfLpRftzB5Yg#Y#IxeVjLOK~+yH1rL5vJAEK!iF9fY&ZV!!c<9av54uHNGTD%k~PAgr$S>z6eWF)<>l}a;0&DfCwx(G7LH2T29L<@>YS2Tm@z|=H1zKR#=f5wRB(}=gq_CVz$R=1FwQA+Ry>G-WBxuI%rKXx0j67J~Ly8J}khR2Z(9DV;)0NJ%(~1cDCTy3mok=p)N5KNE;mxd*}wAeT%n~GY!sddo*BoLO{u2ECI;{!=mt#LG^TpHA0P(&sr=Kpy6v?($KAwWWWh|97nhurcC)wamL;X`zd29t@<jmdI(~J5nuWWR{vUAKz@?_-56WUgG{(hn<JF&u!*}+VxFZETU3tq3fbl<UWBl0pS7lKZh<~NB7}U}m`c$0k%Pjm17`9?TO6Y?SuMsWv`JNcX_Kk?M<oPfFbCc8I8+sFd4eFV^0y}7BICnI9gAy+s8>BHSFiDluZtr`CC{FSU;yyR0H!nzrrqku?v5IvBi3G9raS1!Mk$j32k(T7<^rcy>zR49jzhzCoVu!$i8OtKo>$<iP$UIO+c%XLIY$i(vsvJY-qu7H)e7s8t4kr9(gq(Z_QayH6`Ov4rXBBZ282YOZd||-^`e$@aX9Rl3hzOK3W{rP@oCo1EK_$^i2^`e(X8>QS6A>5%TyuSIh2dl(qa_M;K5)KLnvq<Zq_na62>QcDR%VN?iw};RQ)B)q9-!b%#(3}WO55ma8@p?UqOYIp|spv+-U&9!pZsEE(%SI6rQsY`!j0{0q4Ak2Sse+L`&xMci%d=5o=$7cM|9<(w_DQlEy}bsMl*Tn`dmf)2F-S92ll|YL=@%f&o{v33{0NmuIKNbTw&(DmCQJbUF%<s5ZLt^KAej92Z>p-7saC_TVh(7wJN@N%a`Y%<A^egkBCr9~<UQvr=HQO7nnp<e?O>(<h+j+KLeEb&hFAWB96>Ss;EtK=@HRC6=lcKnGVg2mAP7V0nE+r7*D3a}7pU+#xF*CS%Uzq!A*ZZE@Vk)MKmSaOdbYEXXg5nE=3q>LRIkQd9o|I?W71foqn%o<ZFp8>ZP*)(ZPrET3<zp$M?a)u(faMO)Njbm2#ZWbHmw3ncJgdVpi2f+(<s(q^sr6|?@}MffU2vX=w2YScRt=P`B(=94oH{-O%vr-ocuvf8+KG~H|&OnDWphV#Wi?FP{JJc=7Dc-9+5wlEhtA;N%|pT3(C{O0WW#?GU%+4_VtZHfb~On%Fn-VuGczBw1h6Zk47J!czM9br3^#iqQOmoq%))G`ahBVZfoHAW>gjQp|kZ+Xd-Bb5>$F0C|7**ox45P7WPWmsGuBX?_yK8G$#v+1j>CuTB9PUFpemwgh`^a3iB_W}%n7Z^`vRn8#M?UCQy0KJ5IWi#Sd5mNM{gARbLC*?I%Jq#f)4M1!i(m=f#6|H7iLZ8@v7b@*50#9J`iqS%$G@h{b&D(TBQ>ZsNGT0Vi6lM%=HsgT~bH|3vaiC=M;9A#XskpUVc{0VR!k-I1qJw0_Yb(dNq=!Jk8Xn7zAdw_Ff_~|N3d_Sc4%pd(B*n=`%8Y>N4A|9f8zgqUc(pZ&UWXA0kKyFG^=bR!A`Gb!gZo=h;uPwN68gDoFs{_tE7w%zPv&+w8zwB6UT_>~1zxkViB`*J0J^Dfx2xngFqOt^c*lPS9N40&_tNFuuBQCVkDv1kTZ7whWi=N6%Q>?3LKRcP|8>nm){V&nLJf7EDGy3Y!Xjw_A4D?qZHjGQQ&XM;j|LEs*Mx!iT0mswk!%+(BR02My+ciyr`~Ep&4!lLZFVjKU7*0Ps06ydQhTcsNuGrLZ3bMDL<*gI^1Q5~(QT5K)Uc~5gB>6Nib8Rv9U-Yqwt_|>JsD3C<t+A3?i`Veow88GvM?vBD57?rr1}+{?QH{jpr2NOK7msPr+-8Bt(&zAROHGkSJU~*I;d5!JQx>Hy`6o+CgMj#hD%i0nM6ss9LuWgw@a5&sk460-XRH>Wihe~-YF0Vu@9{Im6MzWZ?asF0Ab9fd|BuyAgBy(zchCM19WN_@PxpgM&XyCWK`|RLN{z?2=d&7$OPFT!;rXS4`)}if6A~7M_0&~f*6vyUf>cD{^>5cL`Sf=j&FFRRIsbHz;s$$K)%=}mtNFC$4E67*<vA#jFs=R0X?7|*QNKymc2$tntnIW*ftqc&x@Kd=2Xh_xh~SCXtXVTo|Cf4V~t#Sq?AMzJ@81Kk_Z7SkP=hG0mwP{V>G+H&WbE6xi^zsr4qPY-kEOL5-4QwpoA!nnVSZjrlKm6OtB^Hu4+mUBJ(1-e?(zLxn@Y+AY9H0WrJ_c98=|vYO9LdVLAltZfuFKlWdb6`R@)<FR9-5E0|nSC4+r&_~AHb=s!E8Jztc-Y*uMWA^E(5ZacwM+&+eLR1RU_$u@S5Is%jhdTo^`kI=Yew^}&91J_xd4XfNTD8W~1Hf*W26vV;!?Pwq5mC1G_eRv~VyAdHgonXIMv)1IM*<>8W+aSoK`<6%nDR|{1O5D^6MZp$Sa)=<cIoF3E8RUW-@3zvKJ_99;zGDm%Q#WeLz8(PoQp<CDw1RPhjJV$ob6ukgMy{6FHNV;$Z7!Bzu&d}#)zm245ts{8gwon@_NmrZ?_|!p<G;kKCd>M`Dq>!ZpwUml54eDan207l*)nF956IcoH>JvR;hIo3qOV42QV{=G%rmpgnk+>0nQ5#|P6<yNsW8Rr5X<UI)>SGPRRI#K;Aw|5{HD<8%9I#~=vSpKld#Rlt5zvLAIUB6Y@&3xUsX@aDmq^>is?w}nCs&uYM98Ci*pL}30GH+p!4{9XYb&vfcQp>E&a+MU;L^*`-ln$e4HHK>DWAL9;m!`><j3`GITX7?5>QqVj~PnF*?-1^8a9jEYYW8C=Pgo+>_Nlyz=N<jRY4JZ(97U#us!uM~J>!B|f=A;ArIK3F%ffpGYwgg*bV~ZR<EOBR^Ng9c1J^NTpKoSy;F8w{Le_R6_<B6_sXE(EWNvS`+03dv15KWT~BM#hEIWVU4}@^7``m+UC8K0&9R+F?zq&H3gKqlrHAt^Yoz5vP@2}X8pZiBJJ6ONof?P5qE+jv5}tiyh6~OZC=273U^-L*I2y%8`i7RWj`W7gV|L2ZIPAx?kgZmB{eGra@W{cC#UgMjg(c-4yXO+Ce$1JQ5RGwv>vOfx<|}yZi+9PYV|6D6Ws;z?o?@%<@rHzvj{)efeg+U^EH(WY;76euLLn7;v|dn3B@TU3`z=QD{(({>@rpQF2bo1515#iyO)Mmrkl9W+Y2;>$^lX&F=ADQfq>RvI)1CPJt0tVch~`wlxdWhM{6XPcq&->vmH0v=IZg(sBrm2g-!+XivDS#%^)?JTz#&sTpvwZsZ{%5qgeS>N$IO*eObP*Ahju;*jjughaxKU0W+GX<sK#$MytU9(`x#aowK=KIm)Le8VDMyulLhYsq?x~J^U&sFw^UI$w#?Oql*uWkeg^;S>h)XU81Dd%MA>nt#K_Ruyhr*r#%Id`j*)ow!wEJXlwQQM&NCg<KIoO?wwx>@R!)U8m(d~TbF8$D+NG)v83t4MxnnX;{|#Ph`qONl@yp1WsI-ie6ItE<vk<3xB@{+0$9^cwEaKAjtXjA%zde-am{Xu>d0-b)OH|ON;W5ga1uRLia3ui(c;minqocjq(oOkO<2gTM`A7XD4m?KvePeZN+FRBk$F@xq8&Y;#P52ya9wPl;&bxKD&WSJVD5Useb@dfQX_@%zSnBfm)2K=6RiZiZvQYMN8CR=i4}R?GfIG{J+37fVXCGtryCHbIC7e5Y>0>z1Ym9RVxd8{^KptKNh$Zp0cL+Vv#+Vg9HT@5Ipc=vGTw^^FWFWzrt-{n_F-Qth28~VJD<)*j1H<G`FS{LdnLta9$q4zjRwHBcb|iXa)$M=Q%G4@{Fk~MIH8q-b1Q5lmA&x8^Aia9%VP#`w+gFRX~JA!Bdwx=E-ijF$mNL98R<XUxGUEYF8~&MtAzOob$f6(G%0rU>ZDbpCJVQbCvnx^sHtf2hY50WQEYH=QKju5TmGoMT@}Fh0#5wy;V=YVvz1^h;vTNR*WnvBbD5^u*Zv-RB*J_V#W1R|{MD5^x-S>WyZ3jmKfU@mGraAZrioi$XL?Kv#a3s<O8FwEoo&}PTm-O*AVs?ZR9?j#K_BZ7P_4QY^kVc`1TbbSiH9-qb&`7&Z3g^in7OXI+40j(v?^36K__KS(}0fJwWm&RM#lEyIFSu4*1DpR;=z5PwI~$SNdY;=$>_{8e0o8bg%mU}I9~1EE^a-O0(x?1oH{|TodVnyY&W-?r?PPDIIaV+JAwhSu1J~Xh`<|cPDXj1cOWn{ac#l20WHN~X*G_}<mt~9*?d8G<gxVDDV0vt0jFA+ZmS0vJeST)nb|n(nh8@BOu%Mi3bfqD4tBa6;vLW|_+oZ}*S5KXDOLm*t1k?HIjZ>~WBAoXJ}HN|*H@%a!xwLn!@oQpap}-C|7mF^rhZxde$YAUxH;PmDS1tw;@vUzY?uj{Rdr##M~`Y8;HZiO0s;I4qRLOTUSa4BfQJISmPvhY+9bBrH(1^{Zf^jVUIzmlMQz)hpW0@$oTN3G@Q*D5K4Es+NTP|O)mUuPK5n8e<6A=}_~o;b+8}%yX;0D#ER?S@^o&A*esmX+7zRK^H%mhbQ6F8_*_9BOtbO8&UYCo9JPU`dD!^Q-zb`y=1(nUznidXRyqahUd=q8`iGsXOS&tqcLaS)^Yg}rJ2CCHKEV4U^uE++N(Fyv4Bpazq9wvH*<fD>Ql`el>F(d9J#sotA+8auC?xI>$XIR9yG$f2xY`g7i6}d6QTh|!&Fcqtz!}YqoN2*m_iVj1ZSXI731MH8>BxkZW<_qWQcCRo+rY{7rGL{c<iHxbZ(r8$MbO*F9r<iuJ(Xn&Gd#vB(N>&iLyP_{P7TjaTsM*v``8ww|58!GVa`BpkXlnmE2gkUbMU@#CJh3N|V}e^;Z?gh%@4cHGWyc%UI$`)Z2N$j)P<g$g7M15q6%$w;*rND8?>`Wkfa9RO>))gDn$%P<CD_=^8r7%+rPdhGm)VfQNBRP58wbq7+vsMs%o>IF)R?`h&w-?)CSrsN*IFWLDa~!TteQfv{K9A?d)+|qR*J1rO^uanK?%-7<kbXZl*YHq)DpP8#|W$y3?JT>N&*A_uX72n3EdgqVeV<Fi*jo>Nr}&<EyJd@X#`UNZFaRz>$|0BOQ9`}r5t4L%9TBPw~UuywG}TiY~nK@7OfZa8rQqfysZ>;IToq6wvnl%=W8m(Spl^`BVhoC%BrONf+Y$XAXTaF)i0Vd-6XL0MOEF76~;)SAYH`6kZJK)G;kGDb+Jwl%&w&o5NWaV1E+};f3pS5fzk7g8$_peM++Jb_-BX!4+>*jorIvec2FskU|aI2s<oUChZgBfP|p1D|KJ&6&;3hokP>77a?WjDo{!Nbb*wio^^Ou)X<Matw;w)`ZdS-Gsn)Xs)jSG7vU7w^>5Jci(%c9(UiO<oc-@)kcDgM@OE|89(QSrN>o%k)mdJ{giX2Vq!s=p1Q<xr9pC(FC7S6PiN2mD;)+-4}C22nX9LzeQ$IsG_ET7k={(z*>0NRg;A*^y3eRbO$)^YW2wC`e}!VQUTlP;w$SI^5MvqqlutZ)iOlU|RKns-wXEV4Gfp*6|eI)8zC1iON*(Y6O3cR?DdMQI&Objm!>f_9%<Ge_mpszdxd_wVmM0-FVJO++U29j6!u*4n$R23{Bo<pB=#pc8SWA)PhK5DSXrEK!Disg(6ZT6m7*V8i3StVRY@#F4Os60UoegJW+>L1Y4Ajy#oFTh}=Yyo$}eSwgEVaRi6UI}C)5TS(B-glUO)ThiLJ1Q^6vNR|uIGl(rs*vS$-f0!jGtm(8(wG>FG60B!X4!MrhHfw$@g<BD*%y49<h49mY+yL;dpnjS(+EQdx&`HRVbu|p^W;F<R*lst!7Z8qPIT?cv{sHv7ORXLTQR$E}RSw-Lx6!URgp;DXJLl>!ChM&WIfC<w*JIU)Gb2RaKw+Q3mDdcjQ?Rc@h9f|<3bf58^;~6tJQa>?7jh9BwX5zlG|NAI?pyS}y|S8E_DoU?3Je^~Gl{4=tAf=EUap>CtKgGrd#DA~DU%Y;-R&%9ZzI~3gu~XXoWwL)?ZvEQLfJW$T==fomLoG%Ls@I^KpET3lwws8p66$usdBOgD0T|_xF)SxdbHAlVUq$i6kSH9OGa~c=9$4P+9qRf^irVoIW5_FM&kvsZB(DAgvdGw9@7;gGmMoT8<Rje3!9zxtS`z|=HlGW4QRH7->)qGE$LdiXg43dY8~H|jAIqbOf5ulv?pN2L1bC=+|!G{xG(j%aIr?J7U>X0^G+U>7Opm8=M_|YM>x$@Jgy(brM64NuGSlvp8yiWQ)PQe68eFhw@%IOj|bdIIPQEjx|?V0y;_V3QFvKE>r5Km!5F?7OQDN+A1@ynqei!yGAAEj=yCV#)Hz-W=Bu-PO?DihS6OLxt|Imo_2v>bl)49sUV*34SmgMj)@ebnu0Vb}y!I1$CNos#FPu%gjyJ}F)v>xo0>g%e?J?RuRyZN^`zy650Kqm}5f%5F3^h$woN*8fBnvDxJ*(}I(l1j1v`qIDgp<}nRV%z4sz(yabgEKXp6GRu@*atxQpA&1xuRMyDz_!<ZxuQ~)qg}MKT1^s4qxUyF`Ik{-CnNXl7ef8(UD@JjACqSh)MgMQA{Y1s349X)646n;;R=Bn_t4k<~<k_Ha8KGt9DLlVHu>=sFS>`1!cjO0V@yNxp!Dmk=AoJ<?swC+veCE;|1l}cU3qFH>>5;C~pEbz@YqG&#*4xrSH_%(Pe^Hnqr5}0L(*iswg=&5ZUjR@ZUBapgC~28LNRTebw%(8%OPiv)#50lnueN?nsHM9|zy2ol+`k^kLjVf^+GCUu~j_!8p5+j$RWIhwO0B6d(kmXeH62)+7WU9UZXfW-0EEx}Yo)e=ia+3hUMaqb`1<>j#&yJk5r@L>E~_-W_qzRCQLZ@JF3DJrzb;hsvcOG`XWCZf0mL#@|2(KXc1e7taU@I=cae1>IIc6zw$0jOaS<qJ!1`iz+uDbRJBIuxIj?^bFV+)xgNW%T`o~+9HNFY?4@(QBXM+2*4YO+I-mh>h4x_wi;3kLN(wNsS;d`Y@p=L%o=n4T<Luo7{^P=(GJPIk=b7jF3Zb~d%Xd8?$cs()eqOGXy-SwnW^lkv8`^ra#QJ8S)e0WJw9gEQW7<b46F4(J+pIUK|)}W=lr`2O9@l9TbNT17I_^RgOS+UckXS08eNuJZ&YP4d$-><c1P`%7i+n-iY!D<qREpe*JGJuXJeB+Cy9(v$4wgUwlk=;Tr!EpRC;})(;K6HUzb9rnzGr1xi)@v21c1F4rQiQOOX{rK^(PxN6+4kn4g1O25YD-wf%O3IZ3lvQnS{#SB(3{3<}x3FZBhw8>QPe)763S9P-jgKrt@ZHolrMxPv@9qT9okeoHDE1I99Qnx#x}Kx|f3eKR4ry(NxCldW0ABb@nmkLx}&4duY|N?nqlEAk)rR{Pbx2a=R+V<aD?+YVLt*kc5#8l=O}RHJ~rU{GMEfXsTi<WwkaQ9lQ`H$G>x_SQ}jo(lMxr#2*4=k<Tc3KZy6(^iadqX;qXUU`+*rV?Uj@Ru~YuW)t5{sM<ERicVY`y{{=66(&OXB>4_qbH(rL5~drq}0<0mU=d%NbyiHE{aiEIA>2C%km;5a^JN!$Rj>bqk!<+^pQZ1`8k9NC(-bzmcL7q`YKS;D#lbTK50XBV;EByT}^Q%5%zmm;5zi^zU@!zDi_TY&3^7Yvfl!cox_UN+F>27D0b^c>jm$$0%0Pbb1Yk8ukbA<yW#ZrshUk<-<;>;2I+$4T{M=S2u;6ktKb1zOTLa<&Vx6vkmuxbxLWUNvy)vK*4{rxpydkZM3;iNOt%hBnNrTI3eOr&u%en!lOsg(9<a9<x$8`3$~Ck?Y)4<eDz$v@ZEp<Mov{i$C1voM7SL0g_$js75}Wc9Xh2AZ#8y^Ky4PSfl^~1JKb5nOeHWMCU~(Le&UpoJQgTU@!Nu76^$5=?g>eh!mFkjWoC;Nc(d=<q|I<5tIQs{E$`J|aJW)d#CKAe2Om;?9)uZKKyC4o2lo|?%BMaSY+>W4GWjL31XSs83FiE>tiYH3pGy={fjU{!c!}iklTX5oCJs;txBBn*}S)*btvy20wn~z&_m!43V)8mzBJ4Mt+@Im*MC^|u)=*jO=M`gNS`SbX=Xsfyl<b`H2wR>Nj>alZLxdY6Ekli+r=Voh)y~gk;&qAXJB=b@w;er`0E|qeYR-zbYoj>CZj0s@vdU0E91b)o2bw&#`8N5o1pb@DWF+0aK%3?|mX!R<|GoXhedBdpV+Q_q-(l`RWD7+cX=Qajlfhv#oS51q$DNv^H0luSE+V3W<MUcQzbEY^X*2wh!uH(>N+!w4z<t!ZN1V9&4wwGk8GbgsXLUDNU%|J{O2gCxOu$en6b8Uclv0m$_n&j)RMd*kMOnak4$c#d3wxvRM@IpSg$H9)TJ46?Vfo0XroW6CCPZ8smn`?Ez6wIekIiD6wT_;lre>{}tf$rg$I@1qy%5MOL<?7og2%f{8_x}sCUxKm')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
