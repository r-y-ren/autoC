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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rk<O^;kha{MoIo`dFtAM4vJ*((uCX#{e(jkQ1s0=$L+V||c)GyLDp<xIbR{W3BlGOL>UuumHG4Et5p%c{zZjEwx@zc2pvr=S1+x1TTm>4%H&@7}+^_;`8oZ$JIVzx?N?4?g|)_n&_L_rLwur=Neg_~VDa{&@G@n{V&lUR++hy5C=1UVXfL{P_EK_pd*^dieDD{+r$1r~f`X{AT$F@4wmYzF+;5!Y@Al&*jM|-@N+shwoQoNXGkq_x9~^M4!L^n>X)v7vhIxnvcKV4CRj>-n@PN<ELeN`0)8(FC$rvay>u(;qhVC-|^XQ7wzrcs~uXiA1=PTfA{ds=c%Kg_Ph5F>yP9bLwm?y;?p18oD6As==SNCam|yFdBb>hw|#H%>kmt}eiz5#kl)4uz2EI#fBM^RcW>{%ySTjem+NUA*7gOS`!pN0evd!s5pACPr+@tV<hk(~amC;oe)q6E=VTn4C+_aHGkt&mAz0<sobh_>?;dvV$gH!~K0F6*lFd{Ko5gr?T<_x>e4NbsDRC%=PaeO&{=N@ueQIdwd^e9f9i_MUH`>&X-$|c0XzKB~tM@u{?frKjpAjB!ul(sreXS3|)v7<b1?!KtCSQKbahtQL#am!>vA3=c+-Pwm>9S890NC;y1Dx=<<60gM*e|lsU{wzW1|5)j3mh$)jOFo%36DK4FW5-SM^Ar6Zbq<@r(-2Qkgt7p|Mu<f)x(c}+P!;t^Y+a@e;!!kQfF@S<||*nyZ;^<o8h8e`<F31;8xRsK7VQU6;Ddf1YEB0@%hJ}4{2s1PfpNg5uh<Xoxmd#+B)&q$)ld^0Zkx(Z*T}V)}@Ko0EQfR@@zz>PK4t*f<;;%Z|GGIERYf5ES9{u@{gvVJSM|odHQ5MzxdtS-wOkLG@#O#EdO>HQ+yEv>uk7>%QUw4E8oB;9v}3NmRm%9+u@qQam?Xs9v7%~@kHm>zHhvHx&AGUtMC86<V;^u@hMINlUo<2gSWZ9|2Wtce(IfDz>Q9Bbl;OH`YiyH=$uC}OzU_oYZpK-Z1f(1(_+3exR}P-Z9WmiCi1J7l~{hTFbw~~GvY{Ni4r7S-!K5qJ`QclOu_c@rdqik^Vr)NG(`}XuleTg-CsHb=ik135duz^N2cE1`-gXT`#<j9z5A>8zSoo3Mzau2Sv{aR3NU{FIfJom7Q1E}0CPS(VlnW7-+Np)jukBaYk0ASAGuy@@tozLTfa~d8KmioxO(6mJ$mLo2of(O5OYM2Wei;*AW`_0eiDEI;C9KtqF*;ebn4E%7;@)Q9O?g}`<COiXY}8er~jJ#w=2^*$%z642h-T|z=*)b72QE@YuO#HpR`<3%MajY1jpBqg9ygK0+L|l%_;6rFR+tSRN@_k)q%|RIQsR?X=Am(IDsWD)^U8AULkhI#d~JCNUJEV<FYA-1Z7x*cNO2<kmt%4V{n;4q7;1f<oTc&06bM*_s}yvekFAHH@@6}YkKna=x+l8s*`oqm1K!JGSk9#s5oki{SVDDGKgllhHUYE6E5c$gA#eN=@3cXd_1F{`YZ5Q*<ySt-}Ss+tVNjYxKdSj7TiJEN_7w?fMXKJZq#Qz<^<^!F5^<n!#a(fn0wT{RA`((@s%yRCeAJJhk!K|B0-CE%+`+ND2L)O=COg99><em+a30V2a-Yh0PvRGz|CDE;RMp-z7oX&G;CP~hJh}R9dV+;6?3<Rk0DyWI#N}f7oQQ`p`%ZU9bW#H4M5fz1jy1vR9yzoh(YW)gaKUFrUSS?#*;`iIpU;8qn(S^c1RL^C;IBkJJIwU8AEpYH%gz`=7<e*3n?e}%Q?&`g>Je79jRUu()ql$h`RBRBUo6)l3C_V#q1aA#j(tQ>y|jDDs^*Pj7HZ9k90;>K6m_RdDqKTTS533iVaO>wHg3yA4~9q833F(%iN9-uJM!5FRP(f$1FD<VCpN!!&L@i(aN?CA5LUf9A6rPWPT=i1CyBOCtQ@Uvhk{FuxYO=34{2)qca+BkIaAeQ|RD;39f0LDdd>6v;Yw25ZamZ42G##;nf@j7+CMQXbtCO6Zg>U@D|SDd;4xVj_u_ZzsWdvI|+x@0>+a(s)=Y{a$aCzK+$nM#&(%w2A+fA0&74=i@3l4^q=R4bMw>T_WGj2DF9d0G8YPBZ*f0obcr?uJnXx_D@Itr5d=4CToQx^(t0T)J)S``3;?UeZ^`9nIBMs6(Pcm&-tswrGeKl$EZRW9A`d@PpzD&9Ph}~zt(VZPV;l6$mO*X`{p9k>xH0ZdTa#w^Y(b9Tw(7~YK8C3RL?T(Xv0}l2ca8$!crwNxn6=B5>W8qzM8Vcd78}&B2FzfRSvE`$1mfV0i0l!cc^|a797(~jtpevmJsCu;9;S7U?HsZ@qVB?$`a}!?+!cbqUmZDnIxn38pjE~A=F<!*vH~m$>@tMEjKUtgWLIPdh0Ub@ES29FoZHYbAfX&8lM-u7_JcJozG=nmM*JayFk<n0RX3qfWwV+g@q8>~0WqtymOip_TriM%&K#hyZ081fQaI_0i>y?CNQ4<B+L5Q?CQuFGpq~4~r7B%EA2Kp~$_JhvssbleG7tGMTmR=)O`@Q#SBsmMB?LihKlvD~F@@ZKw?k3pv9zRq-6HHqSSpwT{5vndR8%l2ZLRbz#GQ03Gs1?G`gfhMPGs)ggrJ(})MFt8cgyQF6Pbz&8<(QaU1{nIM3`BhN$jn%Y=bg1$?sxWUdVI=pKTAHCW%1Q4df;Lqv=J)`6Y<A_B_2bc@A$DbDGQqu!k8zOB2|yP!r;&frn0+=3G$kq{(Vh+MW@cMG#_>-rT*m4Un4BQuMh<qH#APviT*`(_m8P5}E8w3M8SuYxb<EaS{%}OIhT|oqBgpm-_b2+dn@=NG$=&LjIhxS!nXG66%#Rf;#E0DEd7XEYsW-zW=TE{d1ol-%{x1R8!K|lt{q*u&AbplU6<2s#Z6C955R_b><R5Nm@x`WF%Q0VYP3)2{8BY=*Q5Q3Sy5uaa<)cESZq6@9*F5ysUxJh6B;>^6kkr?Tclk^3ic7mra>=dD5Vbajh6ja4i5srJt-TPMkTJG2wXn<^Razy}A#3E|pJm-YiunAF^SFgdoi3>GiIs%)LxIDe0j8d6*Z$8T4RE<`;+)8eexCMLrfCPqdxX%u<7!M&gQlLz?eqv_?aR#ME*ZVS+8;jsRf{^cv-M-z{m32867HR#dU$2NeGnZRfgeJCp`)8%owh1E@}R_rYyB8i{)x3|<_R^7T!ydm0M?8)v4(#4x*UH5hBu>SW>>ji;SynTA*HPS@R7NKq_Zp|$ZEjKFXN1AqWi{^C1@6)mVq#4xSmh4pE1^9xrnq>zn~6!NpOGxFQ)H?=wmo*5>+FB*Y6c~-BkB4)tgZ3Um}x<4me_FK2yRNQBPTMxooRA`(n`DO(=bMRBv8hc}6-T|Fp1=Wb-SXLvqD1a1;lksIt8AYZ8sYL9*HM_A5s6$k#Q1%)@`GM~h>M$q(hcYnI4DlqpW}L(Z=>c93loJIudbE(X^i~6JTC@7_DMQd(v{7~Hjlr*gphKF6LSUj_=rYdJ;)nLNi&dqIO90v#ol6M`6<k_q^|z^tdWM|)*`&iMX-JqcL(kImb?=nMgUEqq5K5b#=C4UG0_*yD24f7f08pu{^eHsj>=U?cY{IIQ<t3sWg%6b`A!Sx9^w+9`L>bwu$%CV8Nhz~xps42wuz1=(K`sTO$I@>`V2@XMU<n#kNEsxzz<(-G$>bDXo*e<GNb=m)K19{gX83Qi@UN~b^5i5s<|HbP2>`N0Srj}5ATg})mNV||j&g*&d6maZ+dhH6Vg_WyBY)6!P(nvyS@77lNB$Y}nSAg@2GWYNz#&)loTQ`Gfrjx|?EJj26*+)FuD-lFc(d++M6><Ku$?QTj~z&}sMkeVNIFM5A&<xI_q3s)VJR`C$9Q*7O>aNPcUxofMd?oP)<~1L8T^-Kf#D|i&-X+-5N5VdiGuM4lNe4tYy-!%j6l#u8r3ZHQD&S(NnPn7(%~F>bjC<IPgBQ<LeIVWQ@QTTFE*cxTh9p?M=i_IduNb^S*a{^X}SqwVpg1+MAn#-hDpMEhAE-Fy0IQhmJgf`r(ZKB2g*aO<>9#XXD$}ngo+9Hmy0KYOm^xtfQ1|I1uQDe=|fNdk9Jh`HfOtvThyPLprGUqPB2z^DwjI!D#pY3x|*Yqx3f6-3jI~ffXLPPOILI%%f~@(>Xd@p><(aAgGZM9O<_(E3?YT7GE*j<s5r~fri(to1chW44%PO{<SG&WT_$UrRk|E_0;^^B3?li(USkiC1Ch%ky&CKZcQs;2#}gv<oOt6Te-q)385BpAB2m~zUOwSmB+ZIgkkfF<W)W`5ti<XUVGTDTeQf#65-I67G~(vS(|~FPFr;Knr!Y}^(3pKMEXWcbH`VDY2cQbskf;B)Y09320qvy)Zfnz(D_KXegonu57a0mO)-=Ao)w|AvA8OQTFggLSwG)j5BUx{@f~ba7_DSoAjAl4=D>aW<74vxf5{f#tQoYQF#p34TTou1IVlCT!J$*3_MhH+t3yy0aTP@rX5DxfHv}{JeG@JTm{W55D0?t}D9v>2`;Oi4v6I7OEQh$dNJizYqkno<br<F}ehQ0q`B$x?fv!^>v)*JOFd?IJAzz9OQkbzuslTE-EfI1#}3lVeJ=M2EXdY2P!dy$LZRp?OJQ*h>W9xyCf#(2-H#+i<~<O@YiM6F$xkAqro>p$)2k;U*9(o|?WV*H2l4R%m*7AxWb$?gXo(Ktx-i3b*ZJrg~d(73*$a&6Vyf^*FEdUgZqgS5$UA;-Ys#ZE~Dur}<H(@??at|X~<(2)S}C$HyYP+}%lP9*X+k~=dR2m#CU#j4f2=|M6>+e~3jieo1V$Fr9<8X*mJr@@1F`w-Y{k0uO|Z*n>SF65GD5LUmbgnfL!(^?1<j4ISl*qfG<(v*wQXdMTF3+omrZ6WMxq%XFWp`h&T%tyqS55#|rk^_$cWM*_kXAI~IkxJgDb^NMOs1fC60an2=^lfPg8{17K6w_$MSHA>WF_X{$KYT6`Dwdb}d{W-7=)s}>lus|-R3wEB&RUE!RK>w>Yc43s7K3Q6M+qo7$vyc~g)C48;klR&EGhz6LQKn6bvEk|15s^L$N~!DcJM~Q7jq|I;<y63hO@g(y7(k6dD>|&OI6WeM^k?b-Fhm(sPvv9yerXctrG-rZ<H>a&A4*efR*Ej0fYNSOJlqhoCscf(Ij(<2cY%_;0-IUwwpAUD)W(Xjb69JOxRzR(q?&O7KS|Y>~l}-x*49*TtDI9WoJ;@h79r;ngoSt**FHt9T(pgG(kbNsLo%oWOwlR7Hnc-vNg?)>?rU$jC25JxuLweMYMRL)~M6{L;<us&`Wkn5`e?ED<gbh>zu_og+{MKXr=%G#>}^@p+#Hr*kXK7^&x;J1MP6K4MpMDc3*$}q_1%LL9@Na<L>{%*{c&mlKngk1llxj9iZR($?X*{Ad|Y_BABJDIAcndQ#gr)62$---Zy*|Hg!U9#b{CJz|E^u;oFD@^Z|#jWLq!M3#dWJZ$m6Li;WXh=yvEzpiBA&&343JZZ=G_Zqt#qBz@R2>ToAyWbzO~s118%45jEOIEuiU-pP=?fO4Pw5bEN790y_vK9(z}vL#-c((t_YiPD;xBv{^FsLw>9)y{&2KvayHx@B1c3U(#rq+zqaZS)no@0U?^guWk-u;S6-2H2OQk^`N(T@Z?4Pk|mIqhbTBwUUO7C8w+y_9DrvT~Zpd^<In)V#C>PYInc@(U{W8huTnl;5A945xl1a51@iNY%RWECMgorq*$hoo`vN=423#FA}64g1}d(nM<+x*-&oUI=Ddi-yYzG&_mqntl{AmONI(n{tkBXWUnRpSq~KEsN^n6UVLw3-vVkQWpU?j;KnV`q5UUJN|AbQOk8ej2E820e5dt*{gt|o@?O9%^QDX{YJP5J#`?@d*MD@KMq)w-7ClJdsDxG>ts>jk%x7klir!cq2y`3`Vd_^FJN`csAE6J&j-m95FtB9UwK@{a7qy;3YXV}9=memBU76MA9)9A=NHTSCvfrZXHtG*n)(pDBU@|vDm(O+F&-IUAH7A2DNwV*qW(`?nuSiRfq?gWbNhTNm><>Rb8j8OA@D<1m#t6&U);ULNcO9)Pvtb(ToC$Z?bK;kJN9Uv4fDiDdhe71IOKX}@rr25jiIyD%5&J(QU#-StqvR3IX5gx0@ibn&mB|tBS+5X76%op7U?ut#?PV=bF`7IQ;EwWnW@@e)UsX?T?g=i)Kh2g9kfz9bp0N4$bOJDzqR-89#Fg8vUp=s2A(#K)B0%KLr_@!HE#D4A)LV>3-?SV+t*H23Pt{L;ft3`RZ|Mu?T9+?YcI7Tc1sLm@!Icth2n?_Vq?i{MdnjLoJuA`{^Ja&dxO_50|tJ4q|X#Ad9+ziMetSgEMG9^q0dhyCe7|K^?6|}O<!=G2!R0*RwIEVEPN^z$Un$_{qAZ2hY-=j)#Y3LxDO;p*#NVk{CwR$J>KG&B>Ucz9f1|(F10FS40oRb)eOgYvB1miqOVB>53vP2k~D!G2l-I3}f`aK)S4jvQe#@oJyv9>evRRiO@UsCT|r5B7&Ls4}wIe2Tc9!1hkyDl^XrfM%V0~=2?V2;{!n)ET~Ym`8p2*~Ysxhql^qK8L=c>fWuO#aZ1_shLkF3mjw4_;po%!d}Uj!LS%R4trY|H3+(b51zx!VY(P{I2+CC5XUPo5={Pyb@03x*X1fXHN70@;R?ccP1^%Zi3Xget{9CQuK*l%5`!MU0)hPOI;CG%EhW_9EdTx^m<%?uoYE5mXB(AtTLVyPoXajD@owU??WOYAHqp%sCm?De2DjUS_$<WAL2A6)Ks<{tmas}3D}%)7ZZ);GLJ&GZq$L3jR+Zuytm{9)HOzu!Z7@(W`y4mjk+QnH)0uW!ZgtY@v%78vmn1r2dtO$%VbqasurMC<N+cyuNsLOAIjINgSkiLry4p`NQ@V<bd>b{4zMMaX%O;loRy|zi71z%@4BWmJR)BQG!)x1I!1dE>03Q7%dT6R6jp<<@x;r7q828=AjtHEvIAP9gRe=LX(%ME1a(Xmk3<#%0(plDI95(2u*}<!t@TBc)`)tj^-+ZvUgv$(>NGjEBI)<kKbTPWLX2H7$qJ?TSBn~Hv6}&^s@6EiAP2TE8WjWK)kIGJTznXj(S3#po>ztzgZ)B5m-r`}(jQVXa{X~8VDKBDq1+fW6r(t25GEKa#$nRwpic=zpk!bJnaYEWP7%+M@=jFfNYjipB@oVNu%QBqv>E}h?~{8`YXAubWnswpHXGns)vPBlNX#5FFIs8$nI#=u@YbU@D5+T2I}JU<tM=xOkg}fcD1mMWGFax4+s!?Kotl0yU;(-fj)(gP>R5F`M0{j2ku^5)qf0_|a}o~&X9v{_fGTS^Yv>hymIBjdNmv)?YQM%9u$pcOkNN<a8}V5HOg2Og0@1m?ys5N9A>q$M0$piT7V@%?8xknLe)Dzetu^|h!t&DX$qWdOe&r$c=;{SHA_*I#Iho_8N7`I*IRQi!B&n4ubEP7S3T4<TeN0*k`n#N0(h~DP`<nk998LVNL~Zc04d6KE<#vaik8%<<`H@7(Bb3Ob+db6CB!zYnzrc}?S@iYnw~t+%gX>UM6zPhNaEIbLuebUB-TmtiuO8O2GF=4+0C$iqC?;8c2{jTT;b~GOY;~1F`EgI8qRg700%G(I8)~vj2ofD#Ic+COpweJJ`?Lpof!6B&^<U3uw6=G#ovdb6Yo8RfSGs+4vP;n9D;fsP*~_M6O*YKR2`KG3Kl%$KWe`86*=46vyH<%li*(MxZu`VEYc_~dYEdXBT`Tf>v<MO-m5;`wy5>`z9*I)K!J*cfbKCCyL=LZ)qI7H0Yc@!DpHCjb?}maVZQWO<$X4QG-h3<weOF2Ywe%1rKb*Pv3uu3GsXHz0B|wla;8-jL+vk-@h}Ch}-SKZW5ZW2H2*VCNMhc6U8SrKhX@-ic>^uQ4DFYmleO4whK^<#v)pnWMw27<Ik|-zoGu-W?7fM=HUoYD<Rh``)go*e{+Dk6)Y)cFLL8R^DLoa_H+!imr^4sFF<a5dv$xc2{vf&JdO98FHXXj?w&d+cWVkvvtQsFF>86;NmD=}N$5rx#}M8XR{;|s3ZWa5U|fXZ`uQc;pA?HWi8J!_YuN_4mW^gId-AT3b;*DO|=5!sG#VF3Tu5tk^lm>q(PaRSoCk4bUwUOflfg;HDi_KdY;+HZ~ibY!;x&;_suwB4qx>>0eSI1x^CffpOdcY9F%a6yUP#!Ydg*z5B<NY9O#d8)j??BTC87tSwj02+RIGCXoh;53vcjA8PsNl4n^N=$Jvs?RXXq=KFeRBKBFWq_lh%H2TcAW~xX>K5UR2J9+~A2XV_+Xy8TQNgmbG(U@O3a5v0gdKGIp$GZq?`uU&h#L|`K(sJ7t*=~FxEKXOUVon(PoVbp*TAm1nXDv|^J(UE6Ta1oBE$WBECLO>*9t9W>}aIWAEhcVVyV6iaJ}trK90JGuX$n8S9%bOr7)t3WZf1ACEkontZkNKBpKo;WdO4^OdYLN5KL>zXd+lQ^58*li9i#BNKzihb1&3sDD6VlViGJEBf#erpRxWw-Se}ceTHW0(=wC_x2&r}Z`O2#lenZ*aevv|cQl++4MF!~w1K9P6D=T1c!AI{$CSb7F-1@mmJwv4^V99w@4KoAA((j7%xlvul$kenYoR>FhJigug(nn)OU9ZMP#=I(D6UT}pKd(b3@9#qr8kkhF*F;~cT)9GNvoa)&}jz2@F*vY2pkY6IM4AhpbVB1`gHf68qX&=qZuCtZy#J#4o_s>mB??>a8oHuItlGb;~plj3O*uqlg}n``@6$P{10(2>Ka%w0}^>YwhAODXCxGdR#Qmn_v(i<(d34v_(YF}Ovro-=Xcwj)|FLg*j6f_B^ZC3#<b5V^md;SSm<e{i0a-81jzw9rB?GW&_bpzXX9=cVuo8xi4}%kS-ESVWJ*shIN>_F2t34nba;S3=+c$iJi!e?`WU{VB$SCMsm)ajJ@P_6M-&<z5Xdt;aa5n)gWr6zTe#;7iie|$i$XHbT@~HW#Cb%%(qpW#oHUL!VnVz>DUiaYGE=gikxezh<dPB#<3b`8<gGdw9(|ZC#i{zvxq%SgwJ{6JoP2!V6Nbm49pMnb^~&%De4Hr^J02Iq$6kaWEhiyfkmU{_4Xxf980fHsNoO!LS$@D*k<IP_&P4<Y<%9^Bi3dAz^v(%{l7=z7D-z%sXXjV6<eB+Pns5gfs8<ASa<+I{j-sWRf2^)dLJE!SBKJgiTK8vL1s{jk8c{BYnE?=NMGnn#7cmGdUH+%VTbI3}uIt|uA?dmXr`?owjK}nTilih4y!C~A3IZ+Vs)&O~wk=#VuJdChSqkY9(Pp#@+Y!W+3+Njyd8goTtSYP_E1g{dqg1ASj=Xi*Ah`>zq%0BlyOv>Opn=)Rz_|4L#S#`ZiPkT-dO2-f1Ngcvev;_N>m+DBeUqM(3f_NH(y|<WOqMulD4$UyrqbjoEpCD+h#&|CoK=Z8vIgp<n<c3<fiXYF)@c(i>ZE)A=>U$SxJK~+w971*`QU(%^A@K@<VvA!?}_mGoR8i6bKr2K&J``crOs{MH3bd|5YEbBK2<N|gt2ih4e-jV)?r1r43dGN6xGo$C5S?-x-zCu<9m1Cku}AewR35L0z6Ym$BDTCvfxO5gB=6T>uT$|Eim%pW2MKUP%biS)v!?#F4<vcRLNxET%k#+!yiSs$t!u)!qK-bP*ZD$1(PoEmx;6DaJSZjz1q%d9A-K!*z?~OtLt2dlSlGe;Vm;cT!2F~Dxz$PLSIiKb<sAu9>T7RdZw|qhC3Q`o_i+#7FCB+(srA#t3X3zysW)~caCQ+39w<N`Fvr6#n3W=8t`Y*Ov<dPtP+9L?xzmznW$8<EHJ5&pt?t66>lYSl&#<e7#>cM*(_^@+m*;;Wq@q~+s|n$14p6kw?=zoa~aHWVG2%C0a!nm?_@inQV?|6*3DErzhe2I*#YseF`h!ziFgSNV1PQ75?ITlFoz&uc>Eg7hH7M~^2W|<ctpr1^+6L2F0a_Es>?Trwq)ta(le+OwxbTpE`<k>E{tvP^cHGTn|^1-T86cb?*KQ5cBQJxPfB$KC!N5=x7eX>v5*N>K2KlI*at+H%WYOyp+*or3APKabx~fT=)8Ok05o16399#8eZ`yA>OTSuw|#VHE|T*LLprfyub^av`0-^n(fObrRZG!j3(<IF5bViCWrfx<E#=dcXczSXA%H1Eih?x9v9&VGb%}8hCm5)|jEpM6Fcl_{LDr@}IhUS#<yzJ5<yedW_%GT|^5Y4MLsKL>m2cH%!A((u;T%FD<j7U)P4R-gA5GjA8sHG=GRYl~e0mEem|6SNY%ec5{kT;eX&a8JLh2mKjBzTIRJ{+3btPEk*=(Vw2fMu^9q546i2mB1`u>@k`X$*|+R~iM`&1?1m!Uu0e|z_Ee;Rr%LA;k}!B!sumdLPRy(!Awn)FUe`6h&RN(H4$eNl6|v6M(FzCVgt&_3Hy;inK$g9ueQh%>MNug5u~qruCI#@hiO!}ze+PXNu6GC=?kpvR)+WaSh(qi{n&Dw2b;4+iHHLDa!IBH&6T{}@-1jos?g&RZ~CcTQkUc=rTtXq}2ffx3xT%FB;!jX|@|9OXAfMQ`+dY*IJ#2~cOKv)kMaS1*dHC_Y>!$Q(Hr%5<<y91!;g+!o4NqE!{~p}qTuCAt$%kgL#zzB|6-;~v{?j$X-5qqB24ql>f=HmunxU<Hw@D)d8&$-`B+vdyAYLVPQJ!kd-RjyuX>1D&-kHdE$ZLhmEsUd^`JmQIvIAb?Yfb~*(CNQe?)Dk=q_C3}g%)+N<^alOD_TCH+LtE*ztU5GI4w{CYdVr2mcnF=O1t2a+(4?V!ykr}ET;hv0o+{wC6Bs$5@K!5ToF;LbWJN&>R>g_XmN~6?6wccQ%A{YkEvvlr*_0pZBSgudis-H`ko!ve$b|od!(arP@nQ1g97OS&n!o@r)<A-`wGuk99gFucij925in)EEXIz)xn2I5;Lmf8*O?Z#XMJ!x<0b1M(2uVnwzTcC6!tan6`?v4~WTFyeLSQdpVO|Uj*b7QL$1!fd0dLw9#S>e!`(xPRvrAa-XRRnkQ)frKsmtR(R33b!^LTJ#iev;9jrv?%A_)ex0Qq+@XXf7@7JCEX#qQX|>IOB(B44X-rVGAZqvO7g>q}z(UOSc*UXn7JtP-urmkX*&^S_rz4Ogt0gr%<)&^$f~tXP5Hs^VelXq7dEH^v-3K6TT?F8A31`X<buY%A1jwJmXA7S=>S!LwK<jFn(JLxPs$LK!C(@9g$@f(Gq==f?6)aCT6gSBqW#Qe;KvVWJDOfE*Tb=q^ZRvz!8>V889NkTk4g9d@s6H&B7|Zz-b?P=xXdq{-?B03C+26UNf<3S*0c=_o>Fek@kQ2v4=W?RR**wN&$}O97T1mq};JkkHXtfQFdU039L1XyO$}fk*Nb`??tUWg(RsG@$W3bSfF6v43I-bIzmub(=?OUcUfbEFFbpKolSsf5&0d<2B&>(tER8u>T^+Yt^o)26qp$1=E!(t4l?sB+Q^k5avk@t#n=&jg$;q9I&*MeX5&zWQ_)@2*G#V5NeZml`*q1C<#`gr$<L2V*NnpDj+g$dLc6iZEJEyZD%U2-fH*}*2GeF@d-PJHp7T_(d5F*6WjiP>(S1E#G|CgMi7OCNu-un3YExZhZ%(?yFGt6<!Ws+!lGRcqp_+1Wj(2T=qVE+%6cD9};wBZrC0T2nDup}eOUoi?`UPA)a^$>Rrch<3HbAYPxs<xApGEl=ii(tyLNS))Ez9pv0UEB2NF@szpad8mG%V@L$(_a;)>U+TnbvL8<V7JmL$+jF+4_0{c@<UGMBxXoq6UFGk1KlBQV&M8FBH;Y!B%N|9pRkII+=&iK5!>n($e0m`pKrj71A7t;SjyQI3vjLqEaf!my+uc>9{Fcz{>(M;ML$2=R)B-=MF1Y(u?Yg95N_nxoAjI$WS*GN2`8-A5R$MY?mVfH+StW#Rp=G6hcoTJ*uugQ@ji~J)!A@?sJD+nH_)6WlN)u8oc!=Wap}?*@gM>=C1hY^p*Lw_r(!f8XW@VZ1jlhj?&~cvF;$Q1ZivWr0=yiOrVjLatKdcNPt~qX*ZDiB1SUwvScw_KzahbF(I$D)r1vMZll!WiYRqT^-31MRH}1QmVcPov)(`zK@9|RnRG$}Kzi<^iM@${0D(ew{L-b%|B^L^!J!bF1EN`57S(TOQ*C(^hI(wtbNH2XV&a!*FaCO@^D`+rV3i40aI7d_pyXi6z~d2F8~0(8T@hpW_`i|!BP{')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
