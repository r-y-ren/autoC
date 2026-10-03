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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rlKU2kN`k==ip=YHV*Di-}VJK{=%9jS$xk%_e+EEez@28{KC>^EcoyGKp3K5m>iaZY9y$=2*s6J#}66`40OGU9yv`Tu?MKmPTv|Nd`({pP>?`I|p}`_oU~{N>X(|MOq}_kaICzkK7DFaP~t|N6iF?f?Gr^`F1_hd=%Ezx?sX&%gQ8cRzpg>6@qDJ%0Pkzsp}f{rQ{UegEU*H|iIE`!zp3KK^F+JO1$b^B<F+udm<!_7C6x{@WjZ`N2=Wdwl%kH=m}z{N+DBU44M>zx$^@{qgbz=MVGeZ=N21`uWSBc=?=v`=dYp{JWRG`uz{T`IldQ@bjNu-skhHuS4+D;}1Wa-`DiFmtB8r#-CuyKH={lfB5`|m!Bv94Tc^3<R2e@{Q3JIzW;BJKi0pm4&)Ete)pKg5k&bil;<#`*TrwLT^2qRSOF5w5Vym{?{ET^{QgrMzx(`TME&K}yO_U5@FLRZpq|2Z{!8Fn-+lYCd0+lx3@!K|SNpQqPjMqIaaC3lwJi4gb**EQJ+YtAgT8w)e5%8HN&<74wY*1}|3VOl2Vq(E2`E0vfB5<I_O74f@Q|aZ#_yaq9*9`7?ZSuM(lE^NL(!-96x7ofAV=`XhoC)u`|~fqKRG;JqIQ1jPCxq1k1v0PoE^pb-PijKB%ShHY6$|(M~~mWd}gveE>hL?CS-@|%mZ-!;)T3ee-2((`{J!%z8SLMb&aq(A7|>@#*46x&nx(kf6Gr-hsNa=|HJwBHZE7W3x#ZG{bGF|)f;`kTP_0!DxH@=mw_t3)mQPw&{i>Sc}Vs}Mq~9ni+f=IJebFH88;*KpB@=<7|>_O+RrVI1=#`BIT;VZ=MPDriv1H%CC5PlaB_%LABc~~?tXlAbX>1HNvB?d?R$G*dB9h&Y%4SD;$FTcuQtuXi8AqR0*Z10TX6C-HN@f@3y<c-p|oFC_RdD_yxr&37V`YAPSxb|7v;NBvfE9T_@~c*dfjoaSIakl%P+yYc*m#kfh>Ib*~?q!Z&c4H=SYB<fZZ<CT(AH8RA8LGv->pU_kQ>JhaVol`}tok&iJ&U>6{|Z?aQP~c3Dt7Jb-vL?2fG3x$2{WYjqvx*q=MyRg(Ca*UPlPXgP#e{lVaCpZr`|qD2ov-qO(SBCiiqUViFp)Kn(2=BRv!g}=mqcy@^(`Q)QM=1iU{<9fNKLy7Z_t~cfLM=v*JviwWW+J>0a6||9b#ManceLAzNxV2r1l;?BTKdH_b=^Cq-)c(boKb7IcPc|q@Mp}z=u8s!&WFMV}aq37=vB*BxS=Nzp`B$vHD?Ew$d1F63OT8DQVlsSOVU8kv9_O(Ly^NP<6nzwSGxJYD<A03keStX%{B8I9fV{M_E&_5IUWiY2Hu$r<e2cQPwYbiDVH|H!`*V8HZg*?)jA=`@G<EtX{d2~L_;jm6RaN=!z{lO>3xRw0RjxC}MO=IDi}9?~e{*SA^NzsL6D?-J^WFXVBefi9lTagtZULVR?0(@(xZC#dTt5-}iH_H|Ak8biq5xqT(b>pwSY?1Cmcp57!#~1q1^INXDyKWYxEiSc_VeeT9!ED8K<oO(p9w}EJd~%+SG|9}CgttzEtV+m;9ZVp!z#0keT&Z%Q$_6PCd+28)-?Ll?aOo{5r9>57i)gwk3&%wr=s$-(4XSnqd*YQ!xjaTOaZi^-+S&38qN%AWkvA)cRLu-!Hq&!%Zc0XzWwpPCMP-$U7e0jZ|xcU@!jWSLA2qg(IO|Q@wKOX8N(z9HDYHO1hk6hPl_&LZ)fWp`ovi)!2}F?ALoEyypzjSI00%dzj?kZoW48g{Rnu2^OBs}y1V_oA9u3%c5p@tYuy^$V~P#z(#6{b56RU}RjB5$PbbX4PCN9pW#SjY)$$GB@;RiZofN+q{g$ULjPveR9Z?SBH@)$O3GN}jO#@MKvjFc>U)h<mX;jKQb{;oBPw%rHBzohs{-(KZD{|)aw#&PebgR-np*oM!=OSYNFJ6+9kDblt`|g}&TAjVIwfIU0I~Pw&x<mB&ygYF>i9**G-}0kUv;kdsA1zv9EgBZM=%!#|T@1r{c`3v0{6l&12X&2v+;>qA{`B*Y-#-1r<Bvc7v$P37Lo9=2jsdRCy{}9@t8x!Ry_R@<sq^ghHglSmbp@Bab5kTk<MV~h#=E22C-T;9Z)u31@>ab<cjdxP#O;baL$?g>=G%Sd#kraiF5zViYDnBhSE22wHG0?aiXCY|7jH?sO<A?%G6-$a(qM@9@rzBXeas5X3YK;95Kf;wRI}300-d$}^<KX=d#Hc{Ev8*l;m)l3b@86PN6$?3!`^#O>e7Jtu{fbpcLYDefKeODOBRY_6^aI&Sb@h%q%oW}Tx@0S_{37jC3~RN1zqjr*rajc%+li{Lh-?6vKMNv78wQSN+I-7B2y=FWyMaM1Zj7QX<tpIdxJ#8SPal<TR04@Z45_YZVYtVISjxuTJK!nyHCC5m!j!a`{Y48K`gkm)O~60_)>mwXi*z2(?jddTuchMLGp0g+sml-_WN|K*Y+B`AGkHLX+2P~<byPtyT}-GXK$GI2R{N_F4K353A>E9(Hd@3K)OY1q6`G<jz(D^EO<9y@o(5@YsQAhg9-@>P&A^@Pp$hafL{*Yk<I5>)nvvRtrT1Yz&0K4>RtPj=R3>}_67C#Oa#xGa^)<f<-U%*d|1o=sZo9x&oH=uDff;WB8Q{E7m)nYSu_W+aO~T@jh_{q*J(de?<pI^)>~r2N%s|`9FRBLNxNeU-64|_*qF37w9n03-eu?&6=`<YY5-SgTJsxE!W=*jK>THJuR;5HeV?@@kdwZ}R4=UCjdU+4CNdV67wIaD63nGmv2oiNH0WCQfdCj3jeK|XhOgt(){-@sU&I=IFrsw35uB5#gr?c}5?6&@d8-(V0$ZOJ3p}{#<ZpSG&*9KxZ`7Q0bxE||y28!fFTt^yxvPFOt0lVHc-Ve01_1V5{>^4BuyxGQx;jJdwYl#Nu0x85%?)aab^P?!IFK^jYe&=5=<eMlAR}Mgg&_w$I9S2?NNP<u=_3WQnL&tpZg_L%b@Ezk4fF<fyICb>y|^#1=WUuk-Laq0*xvpcW2=uy_;c=palgiB6%-t$g<V{Ht7-4wac~#&Y>GQI%1NA_?ESG-M(~3K<&7f<Em0alOxk|@xY0D4A_zZ<j%$8~M?|>-`#1C^KV+D<9(6lHwst!fZ_`oz5OLJJ=Pr{<?8@Jw&G7X_5<K{^m;_o*-|D_}f4{*ak8`xE>b{%*>VlcglQQQsfxU3}wVf~VVFnNsg97oZJC|ebQ>L50*04n-mN-d!&jH$36Sin7^Pgc8!j^sUD-IjcAp*lu6Ib{58#X|m9jk~`evuf^JbnKBL*m=?iMl0y;wpb8RpHCKIK}gaZ~yQci|J+=GJW}5Q$;)-%)tTixP<Tlp$<{$mOCP;6h4DUX)#e}g<_|G$7Hv$PX%qI0;9w%rp}Ul3nk0hhcOndT&m&|+pL?ap)!+c5oS|Vqw~v?&3r&Cbp_v8C)EQP<nvq-ZBh1!kh_w+Q<D94tNZ(Qf3*&xylEYCMBgeYLRa!E%qI$(wWhHp7N$bHA9y&k6LYd{;ikK4K}$)8J*Rm9Du9W473ZzKr!P4mkH7sb*Og$U$d~^t*+;@YdzlXQ1}C2&m#Hc=k{xTayB5s^o@7h%)E`Ok4qXJLgFzOAjYK^OAoeADW!$TKF~Giq=ga<F+cL^Q<YKNZh>P>5qbA?E)j$&2au46@(V4O|E5y>bJ4_b8a07~4IbsHA0dZNe4M`HKsE?a%yE{JCuvLU6N9PSFpTr#-siTOaS5lo?GXx#se%aE)%2nI=lc<>#XCF%%L5_|U34q+(nKBkwEqKhj@ZX!HVCkH@LRwMVj#BDR$^)PrYG@s-hECMdg}?{X?)Y$DT(%<b_!ebA`J_p_UE9cV>b5Dx9HZ>n1xXWa(P5AAWQhr_oy16RqhUSP>KG2^Ml&PWS>eTC=SQ4Ux%q(xL(1KHpU>+_<t2yv?g0P;_ZxmjrB4W8lY!=#8k#BBB4zq^J9Pq^*R88(p7y}0>Ihb$SESLny*ne)m9I64Ot8JF7<u#}s%Ngl>HAG*f86zeIEqdtbVdn!EJmf$&JUf&@I$9&cZPHXIkm7X%6p1Hb2W2CtKm#O14(DA?y!n~*loOZN3EPmka)`E!eF)vBAB@-o7rJl?Cl~LK%Hx+!q>!`#pjL>WDej>;<eo&jC^Aeg%xu8MC!KU!wcG^MJ}K>^KztGPDPsNdlTzhXe^5<gAz;IrI>y)p*B=X3&UkKdETd=_`wn8)%x!mP&<36ILs4*dxl;X&~r{UDRuFD0uN}5wZJe;|1qm1gmDPf9@K&E;*87PaYbY~O9pI=sqS${2@?#|P8TQ`Xouq%hC5#2a|4+>Y>xbx3$<bcV6{ttS5|G&T3QQ|^0v-8)aaW)Eid0QeDjd-Xh;_|JG;=Cxy@G`G-q}dRvrdZ$=B>sZ;e~71bqVolX$5*)fJ*L*({8FHtAbaOS59_d1iKo&j2q{ql0HxLiOMa5|V<mMFAQ&?TDW`IF6)C_<Q5s*@Oq(RJsH$(G@hd2zLQ|pRg^;b7fS?sJM#>MI?Qdd198H4Si^i{JV?(+}qOrT0M^=B`R`j$7#pSZ%Icn`oVzwRKZds1#e%5f6zD?HZ?_aUeK$2n~!TKKoK5vWIBLmiQHH3pE!ir-GcYjKX+K<sl1aucq@Kxzj5^!&CvJ};iL$xDy52z7*w=*fi{)aLR-F|%0c>9tyDQK&9*zAS!wICZu$N9Km1ea@3+)qi=gqN^W_Rg0E_PP`+sOUkw867#y)EUd&Ovx6qK%b*Q2s)LeSGQrqu~i-@<Y4nbm!qPQpRtb#EZKDW{Nhvfqx*e!K7Kt}HhD$56tLpy(1|nhLY51NYn&(fBIx3m@+Y&6lfRH|5*X@A)mx7)(2x(XecPyj#6<J1fpLfKmY8Y4ab}fGu~fcDs*Yrsp@1EeYD4$&-2{VbM<o%~4z%#L4!872XBexP<VPsRMnrhhga?6bBXAXi_@!blj0b4w6xAX=@15GU|dtM-LHfd}yGOE)J-_Spj?zFIQbEqbyB>nk+sQXsfH^zJsx&Hd3^<<747ZFV<t1=vIdpPs1o(U^4-UQG4A#wzB`27m(B31JVPNvX~=yeX*~RE#hUrx1O|7{Zh9&;=scU8tqZ51eFi_<5Jsr!wggn>YkAs!33%F0U(bttqQ0ROy6UC3k3RVog?7$YTjGne>O*A9>TOJJKpzAQ!O^VW#{W2+JF1JmE4y2W;y5sf_PZ6hXrLKxb5;_wiG7(Vi67~%AEnz4t_%Ea7FnoGmkt#8Ud=8A*`n#+4F~k;OqN>V$p?8!#mxj+4#bg-85(kst;2g-azxaYLo8t58-#jE2;ds)>i4ktL$|5z5;|<Ja_HDLu&s9#sW+vhyr%LyusB1xs!6zkg<UD|CJT>!ze~EMA+gTr7eS+Bgj)s2<fny(~+Y1KXyt6tUj^nPzn{YE+TrBu3t6HvM5`o;f1v{g**HCKUB*XUYRMgfza}q;m&B5GcZf0O_emVW;qk9N($iJC`?6En<e5e$;W46RWPyKP~%usj=0Yvp#{%cVn7<H$O$Aqo1qt!>*G9hPb0t(@?2I$X%>DxEW`#`wpcS2x1wGtGWSLnk1UL;PjsK=k=H*%oj6Wkz{|rU(R5HRK#PZ*uPYG4{(}vQ1*IV%4WO9{Vp)&JR1yT;N88zsrlO`lESuXzP{F95K(z%>;7(Np%4P*MgS2esV>ff3x6ERYj3nuBukwR6J2@hz27QOeyKjuPNIu!Tj#F#>!0;pwT@LK0Tzh%t2<%fu5eL)bbf<RqY}W($JN%q(Z8?Ci#sgY}U8wilP7w1BWd)Kd+;@7;$}I|F8YvK8)nGYcHzy-f>gwb{=T+t=Nvh@DII<F=TNP}}2Fhm(E%>PG8E2b%wyO;lXI9><nH3di14Ue|-P2#QhrL#Nz5F#tb;A}D-UK0(oO`yWyo3=6X&SWP1>Ay0FWuKcN<Hx4Ov!Tz6m>QV&*hPFoKm8YX2jVRGoIhclkx6?+-RD?T0zu=8)4{5P`#c0-zBlur%^8zL$>(*gNWse8cTv2VY63hf_T*#y{70|bCfKx%oYB;7O}UGH^n+Dkl$E9Fmoo-mEfGzI+Cg|mf?o2Hgx6&`VI>vo_K)i9~y=4aXpQ~31QIC+wo<U@?vm@0jfXT5u${ArBlmF1U92P>z3yh8>Upk#CrF)V|&h?Idzznqk&uwyVJ?62d<5?+o#87H1wTQjp>$Uf^_MlNFQU2Pf+!?0ELLcQli@6c%>Y~A!qU^jV1ct-yCSb2r?qhU@;C<1yXQ+fK>U^?D}J>Jok~yw|0jn0cil@%Y}k9z>|sTo#fHDcl%Qf%i5*p(g;K70UC>gf~MA<%x*&+6PL+Tkh{q*ZKRArt~_Kh0<{t5Tcn~9umox{%QZ}NOmW0jNKRS@P`+`pnPb_2#kD?V@~W!DLOMDYgfGn-=VcTzV?vKONUnnl6w^SQPh0phvgaQs;s?7Ypu;UnIUQdDw#9Eryri-XIcXEim%l0KAH)k4RlHTdcexlGY5N);f-k@0J5ub8uPRuNLv2ng++4V%Q-X>}!Cyx9_iK#r#I9aBh(Qy!mp=k8aS7YCY;7IcpKb+P1IiQ-S`ab)dp}GX|5*_*0pr(~|No$(dci{?c5k-~D%gJmO4W}JxB>h6p&yE?^2G%?{9?KqTQ(jpo{;p|y9|4M=ejrq@{=On?fbSC^#h_@$_y1!poE|5l%CDZ8kmG?<p_UuebZslpk|dh7G%Y)OIN#^^l@KacgSE!wTVX7Y9o!`!Xoj&dTe!qh>z~+@702y)anP{hGbwhcsTP0p=Sa`>Wxy_<X}AWoR<o=uwluV&g9uOB<n-gY!-xjnD6vCEw}&~-1bx~x=H;SNkKEIu<VxO%7<>HF}s~&<tE~>X3t)pN0%8OlS@sK?<Ih5cTVk!J=3%HnQ9^Ht$7%Md%aLY<P{?)JgTHZ;ud@vQoK~D`yM;jRyHpzhB2!O!zBzaSdgXV*J70rO#huv&@?^d*1}<tSoMB?detDLU-mD<K^z@90-6uNp5(sm*BBdXu$DI@OtOVlicKm~XKmcN*z}6Y*`V@{Bw@<~X;UA0n|?Cg=`*i`)S5>Yx?!eXocCyxM(DclKGX83lL7qItvRcZ@1%JkZ5d02FYXFQ_?!eDjjtZ77XbRiVM2fTnr0QJq&2}U8CvY9njGVBe;*}gO&7tFCIh|tvsh=+++jaki``$4?YGf_=XdV{gs@yR`5cp~?2vvUQNUfaduNVEx~#9*9x)x@Oyuij601-Uu-~c|oyMhK6F}TBCBN-hD#s1lO>1e^UE@#)s&855MqPj5Uh&}}-5G_s9t(M68oxqFpKZ6c%54HFrz>yeYGih-b}nf3Ek?<?nv2t6puuv9;oZaV4HOWm?s9cH(?SQC(z$X@ZzJu6)j&UkqcmQm;tZ2-c*^uKyNL3wpt#ayS)u9}7r+dzCSi0IsvS;8Xz(^7)~5H8w95ctQl*_mtP5EaAnmsZPxmJB4f>@sV@1fDte}HkK)cIkDYcU>5Hnxi_Q8^qnw`vv5}VtWxy#PI40m8`Nf6GsU9VRl?#m`gkAuMA0F4%B*m96If60zA@EX#i4!YGloWTG(!d#1Id{Q*svLl8l-={)Vs9#FLBj2XD8JKuNhb^(#<^OEp5)Te0fYEg~!9$G<m?+X5bdMNe<|3OK)T|i>UMqAmiG<0#QcbGD4A{cBsUHCY5D#!cqfPD$42vkoTT2Ox*!E{G&{__aeg3YGp2Cz3DN$WBZ^sF_Zfwg*j%p5y`N5g>QF$*qm5$XoDZ)n|{EHT1+dFx~3nRE8bsk@#wQ?21C=vZCx%;x@4@Es7JpDcqY95rNC!TyXaxK`%m<hs!9oT5<gwE_$JzrbX1HMN&VqlvyS;7gF3UgJ`pnZe9`k`N3wiAOGnI;azpc<H8kx@$}!jI1W8*awM2+F;zczds?cm_>+6dF*Jf^k1AykZvhEB_*1meS5cp}txQAl*Ce1YGOFRj+=H<(C-r?8r%rux3y=>|16_KWdc4FA(cFGfrp}b$H_-Dc_n#m>L{Dq^ChTn_NmC15<V2`CTb%J}qq~WnE%aYaQQmCZ<vgvYJ`;kRAY>h~HF3oNEKYCev;#{42@%a<qxx2NOlXdZ6%0p?ciZq&24k2n!NXv#Z@Qu2i3<j!x^{D0@~E-%t{r^4?X$`D(giJvdMSm^50R-@u}AU~TgXV^&%XTe3$KD_I+KE#d@#xo*^ousXAJXvQKpP#3)^GcCSb=v{-dLOO4_+}jCdW)B94>S(-t#<vkYK~+6}3RM^MQcCp&hW$#(1QKDZlt!fk+?3B~<BlHcR?OsG$Rzks`kSRcA5DvNd}tg(if(|E?<ljs9xN{$Y}XR8x7L|#Bp&QG2X=T&-INNB8<i3_(HEnf+t6;ulG=!tL)*U!i#cx8%U}RpR-#K;$ph{FP9xXDE!R=%*4FN5Xj@z>y1Xn$y_+M$$aLzZ{=D*Cty~H^+07jWE|ir7I)XBMOIO-p=+eE3=9%<=?v`-KXfx+B7WduKPitay#mT*YvK_6G><Eqo5NRw4{O29DHjOK(f7#KNp?M$(6l3eMDOxFXmsNE;Tv-(O_!7p>LFiiL=@izG+L5?V(pt*2($R9Ea!}PAw9n$uNexE=)uG5__T-l)r718;oKvJ_S`hdvQ$%=sfxqA_k(9OMTW!|$(BOS{=+j-`I5qXF!kE>yidT52o{(Fm6xRc~M2!qg`4yG(Vt?ymfA<w8Ew)4t(rlU;v>J8Ioxr?G!F>@kKtWht9-*$?M#|}(TAQo)Zds@!HMEu#uMzR_T9lK`Di{8=)lolnkly+Kd{8N#g?dBmsy;nt_s{g~WEWJ|BTP9mY3>Hfy=hA%fsiP-NpduTdB6$I2Em#<jihoK6#=|JaR{~_s)FgXi4v(fDVCju$u)+fxr$~t_|K^F^E*<TAb{aZ;T-evLLq1IRr*ZaR$d`xR8yhPqau8<`P`kNZx+880`WK`W_a9WzE%H3UO825ac;QY%&S9QMv^{To3z!WUV9zz#@Zsmkb^hWz$*;2a-nL{<=PQxv)i_HnS@Y;44tTYj|u~CNV)+jT&-vZZS9P7C>Eg9r;!93d7PFZ1-?L#&ZXAR+S<(}C&`z!O;`u7#)DD9GOr3U{X<Y?Ab547v50TBI^TI_>}ip9R*Ml?c8V53$+D$=v@tDZT^F8!W0W*=N5yw!$pXUnrt`d@3csI+49paku=}KGwJf3=>-9Ptv%6R-BJQ&00Myh=*Ti&_U3oCrG=)WIi(2Ms>nSZO{)KH9wmCaYtEKKOtMqv_wzhbwm5we`wS=YB%k!{8<u>+qVJAk@il{Sih18mL>Zb%*NhY897p2fvmsW(LB2<l*SGOFH%u|cKcB;MbIGzd@bP1NU3Ffouelc7Y7@kjbE&%o(D1j*W&u{jvUABp<+-I%8*@sq6x#8~{5B?(jXm^%aY)vO^t7cP@B6*`zFrBw#odR5=#u~H6tY+le-3?5aa=y3N%B3Cd<=8}Yi7Je_@K`;uiU=HB{K!`r_$#h$)Ppd<t^?)>2{;~B2O<3B3-X&pf?ACRi_FN9NkE`n4F@t-{J^F>hm`2!u}Hb98k?aD758jH0&@(s6M^_v{K2h=%0^-VScU5qa@@I?1>z}MCDp|qZ?B9++@!4oBC&QAZc~~o^a>3CkU%~F5C3(<CErgki+)U6ehej=*_<s4Uqcw9%dj<#umRNx-tZGwJ7Hm0gYQoQFAk&va8lLAagR>8MKOul6q6{jgnyUdNZt}>HxEV}Z0~_MxS}^{!|Ej!#s`ptcyhDb&*k<$VCMDZ+8-Uw)M8?_Lm9Nf4Nj>l_SYihtb*t$qdp1Ak!cF60C^3|-YSZ_bif2erHrC~ugVpvw|K{2z*oIg)E<CsyfT(qx<rSinJG&W$%a2YRKC9R^VUDMx-6ALgryDU;V5lx4i#8*2as*_aPkLis5<{B6lf=HDE0!S)349Q(IhT(9b>`qcu51yeGznAOr~s7&=-=8f8U3=kSLN|HemN3wc1N>+RuVyk8G2J3lrAcZIp$sWc0O>Ae7kIrI2KkHjpZW8TW&OCe)-7B*vX+mct5!P2VV+AXlnsO{_YkTFjH^KvIQ3o|t+zgH`lMD2!}v6n|q85g5ud4bLOYASx{jw3CR8ysUt$b|eqV1Mg_XuEtR$+=U%x7Tdh%Udi>_X~a-yyg+BZ-GR5Xq-!*Lf|z`9%p>`M>{VcUv6D8DX+S2{B5Hx`)P)@Re6%A^KLtH!NpBxj_)nE-(Y-ANVF`jQig1;oM>Mao>stq20#~v9N_8X){E#ykyjMB+i_mtR+U&Q%qh$;Ldf4<Xn0TC|!Q#4ZC}@nWody@&Wu?*!_q?dDSq}r*b>%T;tgCb35avEbykAl%Y6)vs4#~J2&0)w!j`=xHv&R(c#lR`5RWP{X62U`D9R(HwPi*VrO`bu&EoCq|`(AjXHb3vQ#xNH20cRPpj)49gaq3Eqx%RvK);>ISnWaIr4w5D8VqpkV+p?m~b$%70(vxR?PB;MuG(gVHW)7Iz!W=<ZPsBe4>JGr#3R+Pp9&=5SJj%&6w-sgzrbU1cM)+Dau4H0$@eBIfZs_YVy}z$VX+}|u3~ve&h|kvmRRS<jimQ1>?WM1YBa-Wv5Rvx`Msv`|B-xXz@QJs9AcKaXw_{pS{XCxz9(-Q?;;~Y$p7mp)d#$&{JkHDH%)+T)8LCBfSQec?SPM{#ha)wQTBvUoDGXQ96@;P>?ju8JoQc3hE(@wZ9~>szq9oaV8GFzOwGUz{LkqVF&jp+J0#UA99uW&p$iNVd>~0F?y4x6OtsJDw;Zby!V7BULgq|UiGbY|X&6TmHA=3=5%by&Rn?*moCgUR|)TT;k8!D~}bK|4az`Ba?tYgHcLxUc!jExdB4HQLqs{fOMPsfYEOJ=fsY3^E`uv%Ngx&WD|Z;);6>(La3oQN%=8trI!dVtnZzH$iK=>t)i6G}#VW<v2^BG$$W6(hXXAe$IvAz8fD8XJQ_Pn`W0Jlr9Zi-M7%n4Wab+mEbo#0T?4AeDF1lO4L7f>v}gXPo)qbQooa!=pI8q>Ozem9GrhsjxCH)9k!?6k6+rAyIju*6bk<3dHB$l=Id3&AEAFI_uom7}{Pfp}DFyP2hqhiYYqKsib%22X<M#LO7a>a%wVnXwm=H(Npu<O8mPQc#t%O<i%87uIWWu1B!Kb`L7thEeD-O(_os*^I9K!6xWc?+7;}dEBZ0r2>^yw)a)ve*M~0sBSw498VQ-A6x6b|g=!wKz`<oW4@qjhZ{_D2qSlpym7()TsL-lAL(<h0>AOck6G)CjdF?7_{v_2dW-q^Lq(KaCB9hCSmNe_Mhy;anQ6V5L1DO^Twfn-dnCdKmj00~aCu9WL?unuZ9k-~{evP}cnY8v44|R~9lx!grO&bOaqRq7@&CVgbO5n{NTBREczR+1-l@A=};ZprbktQHeqEZMzqBw#eB~naqo>L#|dp2IL5cea@8!rFo@!h2q=y35i;t7S@d}`frUrc$e+MTKc43bvhNC%7u?L|5mItz<6?wk5_Y9+nDW+4TK1;zGn<xZby_O%UOm!^2Jqo;(8TQkH;$-f}<l_M;MZWQ7R1qzRCh83z~G_8KLN^|oBsexA&Q8gfw-)d_=XRS(>rBv%Q*$SJ?qb%VNU7UU*OHcZP_%hohRaE8awEx_9+->3rwud>*IF#9L1<is!vQE3|&!k*=jtUy7W$GF+N4WRT1OUh^v3VYo7{rT$WR@xJRq;PL0t-ot1U&5QMp$T51Li}?Ks~S#sUvW}E4XH1z@qI)h^||cX9eU0qqb9Zia|vhQJVhfb8|M~`!Q#PuoB0W6hSiFq%YSEIqhrAL!)}`rTM&|aH#ubO-<m160BCL+H7s6y7(MS4VemEVKJjWFac#l)^icSC51q<M!#g|!J(c+P}wE5I%dD5U&vh?hFwK@F+_1Rz{9;H%_QJy7>0qe4Em^6M_~hllZ)4Si@YKp;b1mkr6s1hxP+X)8&y9^Y_E0=1$~xV+AlYf6O?E0Mc}l>I5)O0Sf#kbm+gv@87y9(*`Ap@=CZvftlX^Ga;Cn6U}&ReT$HUtS45Q2mQCP_BM?%Rntfw34~Xobeeponl(<r44JHR9>%$(I9dyt-7=b6ZAuXp=D2vUsU$~*7-f?<r5I*A#s0_anl?26W5b#G|l5h1|%^2OoQVwL*rPZjHJ(WEI2Q9c9RgH61S^Q|8xf6eiUVYNZUf!HVSd552D)tGrHSiOaNU%+Wv!E8iYXMg-t;)`m#Jp43{3b9iZu$f@4=@8L6^+xRpqAx#4G7E}ULdr_;SpQ4OdgxGFx4rsI(<Ltd)`1<O&SZSbi~zCOD6(jn%)C~0f7~)kD0?UN+8eEV;4B1sGl<AuWakthqZ`3O2V_MHRlUXhAbnIHv3B@UE`Fn9YflVA7g3-yYD~<nVQP!CO@@i>NGd`=a@9^>CicaJ#gxmBUTX0esr{#ETpRCp-9dZz>C#uXmm<VRE;A;l^zuOqqeq0jxF$WGL~Jp3sH4C9_)$Dy(b+G2ZoGLOIt>^wyL|8m!2)&V66^(Z8TNcymy)Pp8I48+(1s0E)yrL$bQx4)oIJ2BV*u<kM;05$=0UUHU(WN;Y8=4+3~-)l+p-jH%70ga+Qh~!}A|n9fkCRj0;@bsPmhUITNr;rV?9v)PS#m5W$W19)TB)ptY_oxx(Yqmv?xwhf7_JD#N_hdN6RZgZDJ<A5WUGNMhZtQ)5Au=d#0_%7uK&KsPu}Oe;k)ISg7R39gRq1P_gyRt|~m{W@SLE7G-vG=wgv$kR0}GeY@$`#`Tu?nRaAxIpA{A{LvuiQ0U4d_cu8!Op*F>cxRw4Z^}=_ipdIZp}}*1zTxCl#HoC34FVQZ)waQfw5-zzt7b*y2iY*>N#FH<Ox4|l-yHMk!)|WhR<__OGlpdEuU1~yP17LyDx>xi8>Qi<b8|0G?}*OZy{K&jX0l(uv$^n6j~rdg50$E-z2&@O|4Wf5Hd&7G~E~C%`skD45c=wXz88rUk}-IjTJC$Mqh!8JZz}OG-4(75I0)Qe1Lr|S}g*R17MjHnQKG=N0hMH)D-*?O(ZDVsvOAzi3uinl{$L(J9zmBv8==URpKAYD=udFhd~c?*I0c?if6@@qhQn?rw=YNV#n(m1cb=FE>>#UzUF-|U39`Fl`g{JAR&rOI?*;@qTHreoleei97TW^{?Cp`#l07ZU*7zWpP3hlJ`=LW(S({eHQdOe*+2#(HD>qe0VTSgImF(g>P>0t)1<qz@A6c02M8)HGI8-tM6?jcE(I(Waj(}<idt=?a^_h&s0_tma55#JDy#suR)?eyDAUO4*?nG%65WYVtmn$&U2TOb;toK{g>*+Nt~KjcYeCH&FI-@c4^Fg*scVOUyXIb*PY$^rW^9*Q^lOL5S4!kIQxi7Nz7`6R0O69NlZH;#2C7D27_}?9)aPw}t{z&)*<$bEQv7Kz)8GTZ>x?2&HXZ~V1w&<)8F!i`{9#~CwMiP4-3TzahIY3Xlo-<E1O-ifUq9f9hfPrr7hH+*Ta>F+$a9_y10{h9QcdQv%~}L<MYRP>zw*9Xj3Xy@71jB1h_XQHlE9U@6*UsE?Z$=BC5zz2R4i%{oACr*QggM+4}oC~V4_jw8?q<&LG+a=W%t(Rs}RTbo-d=O(aNJ_hH(B0+m<8chO6W*Xbz-08U#pJRBom2zX2yG|Ng<KS&}(mwciT?lX!?SFPLUcyU7$_So900st!RN%m$!RYvn}{Suo{7!s!_1&>+LHc525wnC;~Qmjp}F<Iy;0LHie9A_d_XqO1A31kdA)EcmjjjMF`vCG4bjA%)(}t06CGBI65VDaF_96EV_mCcZCXN8LGF3wI4JRyZv(Sb>*Edzun#7BUBBeA#Lc8mL4F(<XXWG;Nh@rJ2rw?*%oMt{^$U1tY>4NF(NIKdePHqj3Q#KBPfxpe~5^1<i8+%HB&QIs!rp#4+H|dTNvc3&?6dpgzz8t%2rcNxhh~`>L@ek4uxE@BMiEz^@+z5>n5AzDA!CQ@>VL%z)3|VfV16uZc*C-Ce190EvwW8#FXpF(gt56HN!uqk{ojlqC!Y1rgpTGzh*_!bO#IZvz&NmAQBMtwnCR8u}Zc4Torksfn8=*~(xgl1y23F_;|*Cu36P&JNF78a1I?0WehOQ6&mN-;Z^8F?r>Z`Bpj=YBDFZ<+Zf7`>GgTnjvOZ9<;vJ@Ps;qX0irmwLJaRCSQ%#9q|1LS~AX*!0}{~H}t*_t@$K~E@RC7suC;HEZJvAXGWc`X9}P=J%I*PZ55^}qbg0i$(j_1B>oB$wFt+ke4UV$i(`&SXz7B-Sflt4S%|wb3m=`yfkNa36dcjArMe5k3p?e=LCPtRO#lA3$x?tCUG<fS<&cIj(QC-+A(<AZ0OF}A*Qc+LRPlEyY|^VdO^dv{Haj>-=3Qmtmxf$E8uU8Qcm}FhIyf`G71U~aNSDIvC>00?Zjm$z#5e@igU!3To-y^W8UTR;!@OmJ3-<X1UA^c+&{JV<wN#*FbUc~N!jIYwx$l{X_$eRr#DrN&zGR+|ZuQ9o6LRr9#)M|1+*+UroTT}&S!m6x!{0+*cxsn|hobVQk^b`W1Y;aH^eXRAkBW|=DiL{5Dd#KK*|v|q3Fy%unsi$f`8#EMW;Z2}dzy!~hC0jIFuOYQ-VBStYZj|Bs&(2|x-3!kbGEfJXD4OLW0rd8sl0lr)J%0>$9Yw%zN>jHxI-2NxRTT}od%aSeeAH((VSj#=Y>*wAsp_95eF*Ty|m3<qin&Yv}YkeU~5s4GS0$vQ!@!&%F|Rv<hX}s)DCC}Z!K`qBH?c9(}KDwH*QFAwB!JOUY5k*Q&g!<NP*m>m{2*Rc7bmvB@2{jGxq|H(x{QaFt12I157WBY~$+#-V3>8llCOfN>=~bn4`V~p~&mGb{D`=MRy_q1KRPGd7nVq?S~eropDR{c3LIJ_mwJvNC+Kv0$LWHNC^i`AEd(Sntzb^`w(r7Wu$jYF{+IihH7LuPP9auQV$p^Nk|%98kT-2^%82`Sa1Ad*f4F!junWGN(#C~1f-sAf80>7tq}g%>M{Uj1eH);v?^}oN6{RYkqhM;Ul!L{f&kGxc=2L1p_P6mD?-g&AXFf(1Y|DeLlpe<sNLkIb!j9uzExi2egj0&=&6n{7F1>+p108M{Ysw}aL`j@0^knFZDoCJ23-$Ok$+k%Lvfo*H+l&Kb+xiIO8o-oq@|ZNs|iQ=HZuI4a|vwS%`%U1>*D+Zp_l+2d3tmO;By6z=7HH<`GqI(lX<B3QfP}`(lyb6Bg#DovPek$xEFg!qfYPj1D)Q+GeN~n05BFX;Hff%^h}IekE%1e+Qi9wdsWp%SMDLDKX%nG;@tTuJKq}wB(`q*!g=5Ww7lV^gt)_(;x>^STj);Q;z+-c%=-H3Uy#zYdtSWIqa^n-?nAG60}qjpBdN{+rN~1eVKV}>BbpWE_zs7m(c^0*;X;j@#2eo?P|r1*Ul)aK96$FPj_AjMV_M`pcpXM39WalG6;fuKSl}_>xlM#U+P42%ODM>KtX<}nS+58xq5zbUDwA~^1HcfvkDSB-7vN(5z8rq2Ladzs_7l5t4n-eAUt%%K5Ttz)cIIAt0}nodWPI=T{YqjCuSmLE4k)%`s%0Wdx;fFu6h$%mH4Uhgi>~hnQALr!DN71YIWKyx!4ZC9SnMoJP@_QV=Jlk~xEO7?gB^+rkjGPYWC-_XNB71No?~L%4&_^f%y<P;zuE~pOgMhn5D^u~*Vo<ar4;$pbu%0j!h7*vh3`wSl~7tfdi(h4aR6S%;i}tOKzBNktTq<WoEVrqgcn{;&f$;7{)zKweObfJnCG-uR~-u17ypsIhlD}l#LlG|35i=_!S2(YRjb8|vk9qQG?jum@etGJdsz;na7!*-P#XGDUZw&G*qYBzz@cZ#GyU?=KuGv>k01)&h5S$ASR!(<c{*_-FipDN_U26CXX(yXO|5Q0ir@eLD&{<ZHu9mA5IDAyHYi+fKjMhrfh`>_<jRF-8csq>+|I9{*GiSjQu;4CJ+L=fj{malOBC7M;@n{n&8?kwZK(_$`nlOgM`u02s}IvZl8hWKUev5du+=&!OU(gBMx{`;V`_r!7#=SPDVs9leV6KWz#Q+vIZf}lyy^7=VvLe7eBV&y!7>k5sOiS=Hkk2kZR+PMp|X2eeu{LV(r3vz=w3CtCvqcfgOEPGAwYs3<$OM$KmI^fC!h2UNuiVpx=MzfRnnc?=l_Cd4cUXBK32cV80aNb&xLGnsvye}Po_MvG{83MV~(SM8CsY$w)Z)_8B`|+(w{^3j<2<zYAUWGsN!UG7@Oe@i8LmRPaj~eA5+C?mW)9Yj&vw*lS+F!B6_?SFCJnmNfh_vp>HX5x)}9SN%@FoZ)gzRTS2`5SPh2vkXizKV&p%CB`9h^zHqF)T!2bZ=bnU1Q|UQhwBT%)VaWkxUp^89myd{{*eQHi)i62rKOBmxQ?X-vU&W4yYAAsa5r-IZu&3Ig_%DmQ!)HB>20b|76K)u<yEx?nEDqG+AfZMK>Wt7cXJ#Axzgu$kL@-5`v@eA%8ib8+LmnH%+Soc@>~h8%Enfx-lJvR9ta)Dm%x_h|!@V%IQx@pxiK4EiyA0DOi6VKmJPDfliONrUz@;9qYxmct-&<l<l3DSdmk~mJqAcl8*YL*W(q_9oxezWZi7f+FE{F&WyQT28B($d%H^!bu(ma~>+I+?7lfuXbPLDY$%Dr!f|M|9yRQh!Y_=PqbWv$Z(GM-@gL%nGVKxT8>x@lchS=+ule#f)sNB}Sa`PXwLXVgAXY^=*%?s-ZiZ&CfU;SZOjWwLm*H(42xWhPP^TpwS}Iwj+dj|PE;vyEwC1*jnCPqC6P37o7<egxeXZWI3UU=Y%O+8a#?xh+S;zCTNBvf?dXmEVTc^S3=OX3?WO-Oh!#jv_FL$7o@ApF=Cr4Up?>k8@*L+Ivu%pV^d5m&I^PW~>N=%`eQB)oyPQ+Jre#b9q5mD=GSmK@-tDDrzKhmfX+v(5~w-?9#T1=)Yv#xf$7hZn4CHqh+m_BuZ@LN4MGAcFj0kA*xy%S1PJJP|=uGEqo#<@%GrPrR%1}?N+CT6;B#|r+7nksKVgMJ96_2@;I>ZCe|x`n_tsq@xgMqoq$Xy=;2!^1M~}|Z4E$;%`jx#AD!lHcNgf_PY$k5%+G@%U|#=!SP-jqphJw5M)jmE3MC+4k@|W-8cDwlWR@&%q)-?jZPuJW<_{@)vDGFw1-ct(x5SPLP*dJN4_~Qj$Ovta@W{P2{zbB+arHqe5M^o*(A;rQ@V$qwZ{_#3K9o$<_9ZSa9x$L$Q$cKf&L7D5Mea7w4h28XGS3?E;b`v=4B<@zOVL^%`yZ<dvb847b4Wb0iq8V;7&nUH(C0v_TAMW&yY9V)x9k8g5+$E&ESol>spF$?G4rtGK@=f(#@bz5<K8EK4ODj_3x{8jMgOTA(sD*BTOaIG<EEO|&d{=C!I#V))q$jEv6ioMv5F2z9GroB<Rh7>4bUQYS7LS5aMmGnWj>JTfFkWHV0zMUK+=;ykRxZx{U8LAa!*0jq9Fv?WST7bvlX64ns?Pm)!<S7V3m;7`X>D3xCRjAMQL0Ce0R~a%8-(`Ik`Vv2Zrf5=VOF0VY>(@&GWF<&DF<85tu)aZZ@=%awV#G_9iN*vb37!$4>Q9vKRU>m9FQT$vRNHR%o2VY@rDcFAtbMB3qo4^|YtMUAgijlMM95#`rdzl{>wE1_@>0mp8WeL;=-|iBG3Ax4&~;guJ70n%Cfyvv6So@&_U;qHRn`C-HB3erh#1OUe|vnMsebzUWwupsz{fBV}FJpiWT{==m{e4(#%EW(m-50<bm$Zoo0m0kh*~?q6AeV{t*5KOVPkCoN=6T`xNAJ%z{m4kff?d<$lM!L2GW3InULKTW?<s6!ikq%5_d5fJg9Nn8Y6eU;_IhP1Z&`5HA=ZsS4&HCN^ypb2Og1Rt6lC30*U+-?H}SBS_*><YX$l;k<Ig=2$m6GN8g{D*+TbsKiNNmq#AdT!-AvltWaY(0kX*9BVj>e&j3Gmi?27QsGyP$}feza`RS6&A5{1d6N7khzCSv%f_V0=LO*gBgv{70OqY{>Fr{%-O0k1f*dtbsH+Jlvp__^AJhJJ!vlR%KRz{cbOHE&x>Fl27;{$e92K*4b)M8<i#pup`&3FELbFil0*BppB9e?t(}`|>hR&Dlhi<)2*~tU;G!o^z;7;;Cf@94mEL3MwY>BN>X4C7G7=}46OK{s{Xs^oS=ZvCw0Bjk7P$~zn)I$neMsjRT!Oy@ggI&lEWKt0hYek}Exuf<VIp$Wk}FUb&JYbzRc@xOMfPr543qc=B~=~K0aNxfd0Ng`SpvDdB8`$90dQ=oC&aX7zIC3VrVBh40DHFY51(wbJOb$2N><$KGsnGI_$!+IW7k4*R*nisQ;MrXMH(o&Amyqh4a(??2Sq#-q6^7+;#t$MBM|5)L@z?(n%RVK+0?2c5gk?3f2W46#;Ep8ixFQ4DH5)9#_WVpyc5>Vx*=^2>XV#vp)#hCFGc0{lj?>n(DYc(ME;{gv$RWNDCSL$A*UiCJHq|N&uljH<>#bS_^$`?NyOa3ab|jl?Td>q56qRL_Cw1qPZyzI$-N8Ae<Qi3cmgn^p&i42WOzT^hAw@WDh($kvQZK%hYumET@uMG>cfu2Avg<`K+%JK@yLgY4*aY^dTHV3kkB_>i;MZLraLw%vY)+4_x0ZMXNUYASTBI7I64La{?iA_Dn2F$V`C4nZ+mlVo2w4O``OyuM$4mubc8Flt@ME!FL%Y3p$Oo`8Ka7kZ?wQ^g#?s5`i%UcwIn5zb-6Rp3=<e36Vl~~lib@%EJ5k7qAibbD0#+nwj^4{f_*SlMrBu<T<R}$8Fa~ydMRkrzD3u=SC^PJ&xz(}cPWIM`-4d|qx?R4!G;dVg?EA6qT_?V)k$ySICrveH?h=6B-j;g2>@Su5@i`JA?0*H-rU+-yZQ3I!*qwCimR1lMOPa0X4#QCr_#2-5Dq8Qy79-oj%4aw_)D}M`myJM+ft=NJ0lCJPt8#Ei4uXlQ%vnqqBR6Sl736h$WP1(_?Vb3N4df+gUWl;3qg6xA|PF~ml)Z)VHh{0`bGL-)k6dp=B5(b@_1v2O3uB2pok<I#kuoIJ?FK#>a9H0rq<$XRiGO4Faehmc1xPSIlP5eXhhX$__6WTXo=uWoC_+5gX!Yv=<`jBK+MJiVgb!A>u_jL+b-^Y<y~6tcNMFqTSr+B2MXf{7UY)Tqu^2qI$EhvQK1jhTe(ic_up?-3<w9jT}2g6I%EMq-0%G%f&w3Eo0kO+m<XO`Q22yA{a90@%j(bgS4385@SboxAL#<=N_CA1zVsqxC>S6uup1doSx*nB7+hp~^jr3SUlana^}Mp7`h(;R2>PoHm<|aRswHivzk!I*VxCzW6Zh-)HaNq+X+ARa2tZ&iOT#ZMhu8l2L!O9GN1NUhtiI`M*p}jZA0@S`Mra5~8e@ypkQmKHC4;WCR_6(26*s?P_+n)7Rqz^$w8BCV938uR%N9C})~`oy$kouw4tAXgJSkf<sx82$pS}P)ei#3SdDkK|ztkvyaCpt(W5H{5|D08k<LCs`#NCkXn=9sjBYLJo{5_Nyd`X@&RgEnm*ba_5Y=#x|87JSriGuq(I3-X6NZuY2CaDGl#|1{Ml?49)GlX7qq++@Iyb{Wg$5ARJN$AKOnj42}%P+U|^C{Uz76qnVizoth;D9xD1E^_?H0S0=QDN8CGYsFxNE)Fsy>D5Po1&(vMdT5Xh{fAJOKV#Z@s3Gz&=|Z>wa-=z@&n&&Rp!yFVqA1PJh0+mJb9qBaR^(w+Z;9`tZnRpf2(3HYkPsLgb}1z-kP<e8->8^PR~uBp{47AX-{JEDFc?WR_Fnb)$nI%61zD!Wr-UQlI%_c+MzO87U*$Ha}zg5y<vP+1veE~hzN((H4_J$rl8_U7_tiK*l@lf@3YgaU2>};rt6}m8`MT9&x5)9Jdkh<SbCmi_=ebnnE=&^M+{q1;%ed`HybN{46_<KcR|-KC~(d-$u#|so6m3GI{4-AHt|*p){&<H3(5PU&)cx0bm-80<U)ia^h*?>3_>gj#U4_2G7=FhQE;MYAStj|7Wu6&k5?nF=jg#ylH;0~u?-I`Ktweu)qIG3+lXWZl|(frV8RvPd}TdwN0{R43_3U;Y2!F*dsKW-YE=8q`+2#oOwB$u6YT)zSd&<%<e<HVuF64A#_O<Typ2u9xqcuu!J_val$UFv(qrS*@ZENEofS?SG)cc_2Qk46i0h}z0}rJ5s_sb7+HLtyD9spipt(li#FgnX2Wo}Vd|CJ7Z6}oNKUUWYF3QI+8?t&m7a+tzbFagVARHFtL}gm<F#yAiiTXuUCZZ$y7E|FNb217TP5aD>7mEROs?WXVX=5`Hx`4VF8c}1x1qxPU=SdCaZx9_GT*@;!;QII((EVr{v%SG!+7R!M<Zn#SMH4P&>5t_b;$KGQGl+PpK)Cg^m<U5PS?-Jk9Bm^4t{v+Z4yKBFRfLslp|CT+wNe@(6Yr0B>3K}}%tDj2q2v*wEg=G63SSr3So?ya`cYwfpjlI3Dyru}Lc1!@d^6^v?^|t;T;0>j8jHp0P}akcTt5(1ajQ6&PH*EvkNi(0R1u@a=xud}F8TJ}+p_~9N}KE`Ys2)O6**AxM9L+0uU(NGL+eo?QMIRL5eTfY-_97>x~dfbD^{gS5wmI!zoD*DZ=uKx3UFXq#!$7|Kzyq>zCFxv>8bJ(Q<7-+kYayQ6ECP1HfkF;&x+<ZRuMqCm)-m$j16XL3FRMESU7-i?qpuCgBjXZVvuFaA$I3ck+my}399GsZr$wz00e1q8{1VT^)>VtZ;CJ3-dm!J1sLqk7+xqs?w)C*GV7)&yW9}(_e8Y*s5eY;bV12Qwm)rh=tGMPNKf81qWTi0qz`n8AqsUNd`89!bg;kNaF0@(p60#lkeVqbtf&y6KoJ4zjfm*lfd?5014u7tzcvI3t#2%lNTzypDy0_{G_<@oCZq*2!uqcfCX!s?8^9mk;1I4*^)A$QA2QNBSfvW36+pVfr>a5HacLN${axs-M2vyR?rM@OY6K@)3$uLWg(-xvtEU6jad@26q%<|Ah`zra`F&(2b9Gh7kpq=xX;)($;o$aM_vUXcT^XxER6xfZcy;+up_<#p+c>T%t@lyuc-G)UugN^hrf7b1xdx6N$R%c|a_|!wmt?$~24zoUxTk#ot+~?>M24}giEj#}JU(UO7%kHhcO$=tp^DVlr-BLbc#QqM462&UyhaB5LwIt`9>~jV-h*CX>DKfG;4w1JZ@76y$GQ3l<Pz+FX-ZS`jyE|5e|-?Ufpd$u->qgTIq{rZw&MNEm<%ErT5Z)Y<D)eyW5jU)iXdr3e=15o@m>Oox0Z;mZ&{)B7I1h6qpT1o0{9LR6<uz=ho=vNk9*3Y10cG^GzO&Pb22Y8an|OTZa|ja#^M<3pvKJ@Eg8Tju9a2<$nwL-4<P7Y)JGf4t9-O74;F_e-fCocs~hx!`V@}92dHL&TZq#AQFLlv-{M^-;A(4Ff__!QG6zuI6h2Es+jfUU>{LpvVm}QAyEXc_GC#i(Z$)SaoEL5529Dr+_l2GS!e$Ps8I&yWLNegcVsY+NwA4bJX>>PZKVEHKwiM%B6z9%*mVNely*c!P<3eC%$E6NyxCQ*gr<?PghKp^&R%D>1zL|fs@<ugqEL}Q8-y0j{V)I8vQvT;QA&vRwBS;YdQPz`1b|g&{iT_+YEbd;n7;iUto*bl$z(({QHKa};!Rcv^TUti(d8HKD3>U108(<5Up&c9r4*$rs*^FN#qb`azu<_i)#ko4vP8PJMFZxhAuNk6T0zH|@*AZTQi$t8j4hhv+yt&~2GZlpds<t`ZXLX>F@rzoU#ObejvSuMfEb{&qTn7Cfl-4ZU7~1kxOIR()l%cSQq0asfbt9h*KHv<ybY*(TXGRrgx|;K|`O%vYrtdpoS}C7LSnsvVwml)EGJd4W=TYa*Arpshxah19I?_kZ<QKxlzRuC&1r`_VhP{ZDHsY=UAKYnQtP1B+*vN~NflHtdH33J>Wf8u1I>xtwEa|{=>gJx#WjbJry5Q-K!z0kD2gf06xm8S;`A$9mhX5;a!Vz{T1()EVh3KkS&hlA!zr6i><(cmTSI$Kp@cd^d<r!$j?clot7%P!_nS~NId<%@oQEZHx=hI7WEg@wz$I%}$7kVj3$Nk$qv~?OR$r#D~M>@h|EK!#;8W0$ptf4u5fqT;;`Ou;vzI094j7=GXMO(?(r0z?V`ugXeD^&1ZJ;u&VGK4fcd3y$#Q++|zb}I`vYI9wL`DBKaBb8uL<f)8Ibq{96XUa_^h)et(us%C|fviVge+HfaE5d8BUGdd^>K}eoI*k)pou;jd&L(Y3pT1KfzcvAbtI8P_BaGYiy}d0Q2kv0M#=RUh7|ClGu>1=n`k<Fj%T=3t$E*I!fBfbD1FTrVKL')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
