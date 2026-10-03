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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rM%O>bOBlKd|`^I(2RmiI<WJ(e)CDM-{bW(~nGu(McTF?;atZL$A-IU>9J^~=bJ$gFBg_MAjC#eP-wvZ^v8BO`zQ-?M-J^|!zO?YFak`T6YK&4&+XpU%(z<JbTCxBtHX;Qq(I|N7g1{_TJ6fByOG`;UM9<>se1Ki<4OJ3o7QyFEL<_;mj8@w@l8uRgxKyZ?OqdUJFC@3Y-+_J8o<^=9*K@h62}eEPrhqfx$j`R9-C7Gp@p`(g9;?O{ZpzyI}{_nR~ELo&^W->-)9{l_<NU;T2wY<C|&|Mh+(i%~A;$3Hwg4FA8+Z->uuy;N^+UT)Az{e1S*?fbjepC^od+HOAFEkBYg3#}l3b&vny>S##&hpwM~9#=XUnKz7=H|w_*zkauL%QtWs&f`uYqxi7dyt@DMA2)Are>ywA^w;Qd@=H?!LwTG6TC|5B^oUl^{nI~wee~S;jJQm2;eNW?Kj&y1t0!)5)-(NZ`!Sf}+J^CZY;W#1@5!vQ)!sb^?u^w`3OmGja$N7j8+@3|@+omByH6gzzy7{=Ykh2J>3mm@J07LC_*dH058p|jH)!hdxr_HYbM5_iAD<B(Z?F9E@qDRIzs0KW&b7lwYm+a(<+WF_cnX+WJo-l$J3jw#%rJXP*L}hWz%;{4wO73IJa)&<Uug28q1Q2OeSsZ=7rY-G@T>;s3!a}pt?|9t59DiK-oAaid3pECpEmFB-n@PDub;=2_|BPsocNcEuk_taGE{mi(=XbeeybrR-d8xR_#%1kmcD4=Q;yCh^`)=g-@eNZHU90)@K)~mW%7VW#|@uPrS&(w(8rlBen9h6K7bJefZ4|nFAnpU)4uelZ5lj!aBr^R_;^^|@>j?A1zhB~vWCe>pDhc4h=Ip1c^v=I_WAt1rEgjP@%iqH*=AdLeCX}$M<);W-8}>E!2NrW-x6cb`j<Ep^KUISu~S^B|2$t(@duh%+I**>=tzJFlQ_W1#p$~lMP~vWmHQtGzCgrLl8Iy=@6N3K4Qru(1&?I!FpPL{Mi_5C5yTnttD_rY;Sudy%ntLR$FT;mjYBn}(1)Q-nJJ2St*Pq4J5jVVXzGUTzvlJL`@eJs&cA*CMF<4lKQeXDKHR;(*?zxy|NgJu`(93Be`hdYWbuIJD8T#yd<@32TI`~?5b@*PBlZT)JnYpI4(kTbo#?uS7i+jq%e5BI*&lSv7b@a}H1!Zy51gYbr_`EQyrTBs0+K2bssT@!4@m*gM$ZgH_iz_Qv;IBcK*x9fw?lqkbP)cD{k+3RPw43FpUxb;r*`WuOrIrB`x9tN!^_V51s9ixO6faXKWTqSv6~T|j{^=O7zYbcf;Bg%xIMnWj!sYss1Py+vd_clmp7*be+Z=lnB3kv4o_288F%E!IT!Dm{T&-;#kZm}6y>X+L~3xn;!7QJYT07YH&94S1Apc4)syFg!h?<{0iD*vSHf7p#~zg>9DP0dzaGpuw35kl*`{guXKA+YJe=b_6n4b#D<G*)g(H4bb0|;dSq=gkWf$`+a5f7wKbhNkS_hPK^ah-xswbLKX}YKpz#@YwChua@302>ZV61AoRDqYqM$BDg2jg*2TH^d#W=*_R;KcxAsyxi%0kg&18=CaOnd@};DH`tTo;)Sg4G)V5f9Eb&)zjL)Jr<p^hqyEX3Pyp$axq0jei-p)!BFTyxO5Up+#;_gYl(T>>`sv|rZazbIk}P5br>B4TX&gnJOFgy$sBxt8a|x!{fG%Y^#M<oX@9bmdlQtUzNvJXZMNAkr!Plm|8V{?$bq#J^1Qr<fwb`YDXdy8n#Q|<{6f7bhT->_kMX3TZmp(84!BW-E(y-|{R;;4x)wsr4F%BeLJqE*mj^Qd@NSlHoyPpkkAjo%QAu&q!N)<b0vw?-+={jZmY;q!hUlWZD4vQLLAK?UA5lnx+Z!*W27~sp0_Ml}9lghB0VuN5&QLr_f|Cf|2%;6MM}fTsXc>ed)|(IU`7;>WC)YZd^Vka_)kEw?8u8~DZr<>>!+Sr4i|u>gIQt^^_*DiO>djFLc8>C&CT@Ms`Fw=|MSpegJ*55^c+PSX#Q_~G;`a9bpXa-S^M0?sI;(I2z#SE#pZo$>^_<6}OQaa!Y5zy~T`{Nw?kTw50Wt@U%yzw#V5fn-xPMeFWK8ZA!)vS=oi3o$P($=Aa;j%`EKXUS%xT~6tRHS~KWtb6X#XF$JG15ooZA6L@KVaQw-%sq_7*`^4|J!SmEOZ@aS?=)yq@*Z=)95hA=)vh=#Q_|$Z>&px4gX2y0oJ7<fWFD;bGgoyj|b6;Fya)fVf&NPJeqnZXme3z&)y#oYJxE;>zNVVOkoXgk+WSkPQ4zTD!vP0>yiW0UeoAvUk8`OUn#g24l(Q8KFH|S;dlIT`-C%Ph(Z-xX{(n*fK+TF`pSIr$b{M+l&TFAHYgxG&T|5gYyT$N~4?DwwwKYRy!Iw!Ibw%w8@5#BEyW<>Bi-r-sU))Igt_C;kw!+<2^>~CLWtIYa6`t=RKvAnmmsxsF{`7wLqc@aQEa{*>m?bMNEXF?)WzHFr7sBC6RS3q<GO!$xv2wpegDQB4rm5n$stmX&mS!d)=HvyaHn623$1m)DL8so*8!(3iM5wv_pn-$Pfp&94`!#53$r~^c&=2JTYFN`N?vupkLq!OZ0F9yLta+`jA&u7jl#|m6Wg~<;mALVZvNdyhszX`}59^xC;4sTHC+gEwy3=CXbmyyG@!w>lV|qifLAmk7PwmcC_Hz4VAu}D&gewun<u+D<|umt%TqW&i<2XzVW$Mh+htY2q}H~r3en|^bjJ4<hP-JV8jEZxJYMWr5RtHJU=|@?I-6uKf?%T=*Ks2|NNNqDTV{<kzG4GfaaFzSr726mbPRi&+HRdRRxYvdeyr-r|e_>5rAU_THZ*u6XwgAcNVb@tV&yCYa(3G^U5D)K&LZOeaDC6urF4GLwg^4lVeV9ybYOHdw3@twQX03CHX*KcRQM(CwVS%9_!je-*t1R0z5j&pQorULDQus^~gNLhN5MZ`S==DuU?)YR}cmGaxkFf;h$peC(dhth>;{6kMz)W!VC#~H<ucmMzL@}D=DW1sTn_Vy0$-h$|B>CgY0}3<GShb4B=I+q&Gs4>JsN?*Pdkz>G?Rh@SrtKJ?!(LN=d~6D_T$7Hs#(Owfatj!RhS;lJc2&B0`L(!FXX)8ErNY@pAZFDWL~zQmrlpv#E}9VZrdo)yn4AT=RI8gGwWUe0Y{o&Y~OAyN&wQS@zK4;xE7A#TO>zr{K$lsO-)W3M*BA-uO+8+z;Rx0`VHZZItZ#?Ee^gDz?A6HZ{@tx+(z!fi9&9NY0L!8ACK;S;KHGssuWjeP{s{=q$2H^R|1L!%#nfNX`X`eh>{m+LP}15SU<MBxQp<T5D42N#9WE%-FliL-%W`!F=N^m(eJF39aDXz!>9&E}eETF-(4F`sS=DONu&xcuBn~T7Wwl-P*tTS8smEj3R9k8s|MBcvg0PBU@yyO9O6Jhal7<Vid=w?l+=xq?I)3$kb)WN*U9a(Bh#`O)FsMB&rYvIAeW2$#c<ej3AxiXqGn`EAs}xnLO+$g{n=@<hi+2wFRHo$JwVD+Xrw5IM4)s@}1a%E>(_8KuH3&qVr6S%G?_5Pbqz7#KZ{v#F!L$3Vu|Dit1eE)&ACM)Y@6HwaKB^f<lM(B`!}66jYRGu4^BnI$RS!Fj?i_RRpt1o|p5IIBEdm^s-EKxQ`fHfa?DTo+b&_9+Kx*{_0Xdyq52$+zlWXlQKWAy>*Y+GR9YcFA}@XK&6-{v2Pto1RYXKS4a%zWqZ(+vAH}{<mOo2#bpgcf_;4`0s#L45Y!nT&jlKziveneZOS}wFrz}ldhRpaG*E~OY#abUYLW^8WUQUX+U^Hsvz2v~NnuwBr!|Z3_@6@)i_RjUx@0r4G{D%wPs?3F#6|hcZPJ%4q+ujRV2w_XTe-F@K3Tp<v>^-RHA#rfa@A9VR+XbAabWJ$Txo(%HyVOIkA(;DFo<YQ_gM|?_=!_s3}oo@-hF%u4-0278Myvy%tizAqD>;Z0ipU*3Nd>*==HH%Ue4&V#ZpVKmIZPJ|BUFz?|k}#+&^7p29p54j5-bVnjRmu<?;}6t5x}+Nge;r+IYp!@uPVY4d%BqJ2p6yHY0_uBOvC0yS>~H=xcyR-2Cv^ha7D|yNy-4qQVw)as(e~v;or8r+hJ*jaybN*BmzvMQTIZlm13ixg;<m<$B9CU*G0!ph~`eyIT*fh$Lx?PWN4gE1@$NLqy|wRiK_9OcyKy1fo#qIZVcn0nrRUQkk*Zi+~nHvLTXfH0bWfH=}Fd^3I;X$D-#<*Pd8&I79jN*dLLHhzQRHqIj+c!7d>X6ds%Ya)w-){4@DtYJ$|u)dN3}FyE(HJiAa?o!Ie`#-csx_cjQOYXrK?b?PJ|U=1oNuOaokZ5@iOkt^CdDQ#AgTXPJE<48)Szy?)d2Oe^~4Xc$Z_uugT_Ra!mw;mF~PsH8K9-r$u$4>@ZQPj<?l{$Wv^g`3e59Kj27mn{mR+punc$&!p)`>4*TDT<F%4>ax_dFUuFidXUPG?QV@lZhLVj$@9OwUzv^e~OP7X|4+zQs{-DPhqR-g&*Y<OzTg7#qqej3MI4JRD?_I6tuSsEy?@O|+j~T-ORR3<|4Y8BESh;rs|g=7d%fl=`oA1xskcerq=lq2FF(Gpa|?G)U1qohU|!TbwFIObECj{Hvhy$*rD+Ythu%(RSsCCgT~dd>MXKRV2alWDnV&I<2fGaTMLDwzht12P7j`$s59hOI}D4TUZJ@19k9}$j@LSl@+A`ljF8wxYws_i+0D*Vv<O(BLl~^(=m?Q6gbb7HKv*hDGvfic(Rn-KvL2C0iF;*C0M*PLkDCS^;wz+Ai`x)3;Z*$o6W<m^j)hZWn#5dDUDViP$R0^^xf@`H+Q$DJ^OH=suBw4{o^=nkZUrk0)1kM`j~<=zWytL4?UEH-Ybn-^kDD@6G$zCG&Nv{GKjYG8bYItfEnUK2oxW`M;>I5`Ltx&AI^-+O8o}t#lbbAN$nK8))}t7`QZluv0yG>sS$!#pktMP<1sSUI*C>5DyoSuaQQWHRG#52WC=AW$rIn@AqsRI9L1)j^hywcNPIs4s}$HZg$a~{#Pt;wv7?KMu*MtU3>MIP8QJN*dgxT5GA8WC<sPPtktDhux0k59;abIND(kSlG*%iYD|2OmlHpiQVRv~3nnr6G)u9@}bN){mCoM2)ttKUsG^-eIBF$z3C^H21Sn^#Geyxg)nWg*7@g&~10GIrWfNcMws*%Ar!t1Mud~)N*vy&5D!U2S6dPnKb?A-5@^=#Q;43tHe#gi$h^n+=Ucx(bm0ns)nWi%-3YIA!m29665Y_(+3(QB3TA#eR!ED)Oa7jk(<u~>;p>`^`#Zx6jeU*G<+y|r0iR7eSld<U?wv~l2-W>wG#9xW9K@10f-HWWd@+NbZ4auP~~g#{_Sh%CSdpI@gFHWemGIZDlYrQGWhi^8cthKb^M#<I#myM(ZlGPC>sAu;`SJD5Vvnxzh@0tAL!(L#f~#4?Sqd*F+D4?J`=?&8|L8?(>?$zVb_0tP5J{OHsIpqj^RjBf7C`uvDPwECi%g+23=Sh*Mx(vB&L+`ICP=Y3^?cwZE-feewU)Y@9L)~xJ}23nC`)w5uqfFoF0o`MrSsB4G9rWB9T>r~tx1G~(sCE&-Ugajr4gq|)1<PXFX);;H@pINSV>y-KHkf)HRQ0zIX!a)wQ-iFDHNGuRhOC7FLiQ9y?XQEYT4V>g;RFGo#ooph;kxbx&Wmft5r&c+M;G~#!QDlruhU?=;X@wRk&`4`bBBGHt+Hq+E$IE)Y#u?5}!!Nl05?Y|AP`ucG7+?Y*79ajkEQUD#FC=WgE|!B7_q@YaP@F0Cd!b4iL5De_I|j3XccF7tAUX}ko2-W6H&BowYJeTUGh^i1#-dm9U&8d^-KyR-l&M$Y7j4K;Q7sq#7|kJM8T{1=(A2S!8RV?qMp3_4+qksJqE&&V#2GoO7{*kTDQzLT25!?><#bZPi_szgH_v0KeB^Qzd@WYjSvAD8i~?q!Qywt<IIW+V`bt=K(61SE8ziX9NGLYrWCatsp=npuoXnG4K^Ac8ZlkI09{_C)YfVB70+`G~JQKz|E$?JXk1X6KQpnTFLI9I0`pRCVh$Roi$xihknn-z3VMl#g>(RG_ENnob&@Tm7fENTegbpmNXJ)Q&w%%(;u3n;2aAHZ}#C&E5SjmI3RTOC|W^eEmPQVa}l{Kc~D6b=2u}0u158%@Z$9X=C;{@F3snMJRmCpuiL?xS5LyA;68eMUn`-J6?BP<hlgaQRX3bahZsY5a*bzk(kWmo}x&2hno>w~v$lu}`<m*DbPs?p*ng4#NQlF<zV8Obewf2@awLdJXrS4_sl;vl5wi6#UINlxg%tXd=SA3SGsv{!|jzhsV3mfVZ>-soLI#~k;pVrKg#dA{PX6AE7y7};PqmuOdb*RMM6NH^iS-Axui_3HGD7~g_~$-`z#(}_k>ZTeg)?aFjixxDA$*M}}g5jSj4l{X{vf*f*Y!6|jBOV#e-8sYH=iL|S1cy`7)ya)i?IfAGjL590e(rZeBOrCp(w;UTT=+Z&OR0~i|!mZTu`!Z7Iy0Dz-JyVz+jcFk=(kPWdRV7qdVE|_1I~9qhc<C=ZSwn++-Wvio2%pcd2KXvDg{)bR310<k`^MZS?P&7|&-6kZ*i(zQsfIfQfo26w>o&mxdpaLdDB*paY403ItVGY?+w}ylr@~UlJsBrgKJ~Oqr1~QKt3l=1s{%&l#}qO2jL8m+vDQLzlLnOJ2T3e}y9VYZ!#vmQ#0<;DznWcgLlsW;FUxQ^h?Hl6ElfHYbwtD{I#Nk0j8d*-=M-PUhbw=Uz$2Z^;Hr{5Y1d%@5#Y66cr~ua$^=O%jiynGZ}$s421i;IWZSY%2*eScn2G2{(9(a;`||}<C(9eE(9>kMR3rknPU#BbYK0RX{9P@J)xqben90Tw6`=M~t5{*hNo52a+5)X{8A%^eD=LWVJH;hj!D^t<OgRH!=iO-^J<5zP>Op(;fF2ZBtO#WEHFVtDDsbC8X6`Fz<EO*kL6(rv_#TP@cPd1Lno$C7VwUc#U*NPRsoJU7FxMJS#jBXoTBHE9I2s#4WpIhn^GchHsUj!;IPPwKdh_GW=U4lBvw8P;4xWIda+Q8qB&ke_`^UK{#Ni*IridaTH*a;Fti`vVd@q-9Q<m1kUYba6jH{wn$n&=NHGM5>ue2+T1-K_d5m6~k5N&Y}8IDF?=?O!RY(+n>5CeRVSo*g`DF;)oZA!$ZoR9B6zIprVm-`#&?qk|a5__3TM258$_66x9D0jbhFE^`$f-bhx9;t$R(LR6#tcx%&+yfHI<CK<T$?#rkUiMSQJTZvDvCie%Yb9#1d^!E2&2B@r-So~rU@sUj7bO2+AFTPpxYJF`B*`)l^(orcbu3ttw1UyI)jWJ-H#KUr6cwe4GGqo9SBgdFC_=`~WtLLWgdJ19r2Tu`?(ve>0YUG;x>8|AOZ`@za=MOItBltY86>P>(!n_^DIpyun>~lNmfQ5jr&hHvEr&%}PWVnfx0Lr=Wn9dZd!=oYVB8#D+5#Tp9?6()3+|C4qO1LX+^um!^T~M?lWKdON+tHBq=_$}%tCwT{Nsdt_x|?P$Cro0!?|(Wgo~_K)G75=h@)fDEv)+324FFcHQNM?Li@LgDjYR3Mxjne7y1${jyfHqS-B$@y{3#=G91@Smh~-mdZ%k7oUqB+qDnl3b&>GZTD<BUC3cB@9sJT$g4f*WGfUn^Hl{EA=PLj-0#YV*-4J^v$}1xx687e!*fmq5qT!=f@~Nmzu_ws}T8uGeH?>q{G8T2E+q&KnjD>hp9e-hMgCHcpPPd)EPHPF~sXfUC$#FwM>F^L{Oe2NZL7pz57EQ%kOR)ZkIP*&idHv{DW8<H>ztsjNcpVHxl<nzR$))z49&AuxLKUeQm*{A%Td*D8NQXlZcBPTnmn-|!xIL(}PO6)6t@C2%aMlm_11*+&@lB=4PE5wrauzP30&HcVwQhx%0#1}CEKMl`DqjOJMPBKo$<8kOx_Ep8LMY4FUQLllF`Mte|3>TgMdooFF|ph7OchAkHv02yjVeY4qNvo0t>rSKPC&PDEj1vGXRq`LI+#i1j|rlIE{J7vEj0*&7K?zr2;6Q*e6G{9cgB{fc95{yr`SiqWvP^1<Y^e#>kuYfrYo_IzeKkZp!pt64A}j&f)3ATR2gSmab?X*a3iv6`~_B)dF2(kN}-9GO2pN9PO{yvGWBhl=huK!81PpkwkUI>5olAOHpejtFoR!=D1BB1FRW&(t4>D>$>Mf6HuHmGkZ_XM@jwGnae6nf%t9PX&S$xhaVsrS5rH8IP1Fq~)h;v?G73F{<x>y_DeUbNFnE+y?+30p_{_u0*17~F%F?g;%IE#x*@m!1MGEJlI05Z7r!u$%OqvAIERF8@@0<SuwgBX^T-ov!i}Rb$>!c(WTPCCj$Xv~*w9M<1L>2D7COS(|8n@r+k?7P8RW%JzS}22ISdLccc%8JnHuhdYXztfJ@pcTpm=7vMVOpmiXMrJzQ;M2mI>Y3n^F}Qz4`#6YJ6l_d92MeKpP^v1g$Qd|B8O3)bXz?IGp{<D&t4ge)ZUwkc*$}?Uifa2RT7Sd#$N_dFxbd8PnZhGltr)lT;7UiRHCIR&4g!FaP0D~we96?UmPir!pS!p?`nC+EHnhL8&S^na1g&?G*gSn)UU03q#Sr{H%@0U7Vs+d6G59TZKUY7Vh4qS#sJ{h5jiUKJL90DJ;C63Sw4!I5Boz$q}~Smq-r!>d(=yS{nF4FTX%Fe%43fk@*Jf%m}rVfwpv}BKkvfJNeq=Q0enoPr0_ov(1)iQPuo^|r9IOaE3|y10*{bm{g{?>QjSVY{I}W?k0T<3bQN5|B<E6S-P2>Kc(;&<C%nVHOHGj)4zBPW>QZ7*Z>+Dc2mb^m&)i@tqL8N11OMDe{J5Ke^&DfWs!T$aX$CcG$;nRWvCHtay!z6PrjT%Se8R=<wPOc4uDV}z-Y>_YjWuj3a8+uyFGA;JZ!OR;Fi~QGW`|bQ*9Vu}S9Xm_b71@*1S`mxw|EM8ouB)(0W=xLz0eJ0<9YD;CH0wmia@IWZ%V#D-313R&A2xq<h1*5YGb!c99iuKBO{3FSI7~ed{1&lsZe7sr;m=8!>gI3E3E&ePF~r_XgZD7$?=8_p$x8|!f0>iiWjPMc1cT_UKSPXRHGQ_oc|#sGm|n9%I#!ZIi;X!ik>*|bymXexxAB6y_90N!m<F6gu8kLx!&Z`Sp6E#=rDSLFI{^0(u=QvSaYR_HJ2K%I0dn0WkeShF_{;0y7#DasKvz5bk^ZUJ$^4e*|B(-d^<|6vD(baNRcN=2PNAG^F~>aZ13v?1lQwIGD3}60%k14p5<~6x6GBnHY=@BEcKa)lhT!Sy7Vj@T5#c?0Coc7vteYsxZoVN_&n5uiUVgo-@ztl2U6t(ZbBD%D;kKV!OJ|UE5s5;KBJBu0)xA~0@#2AfEHOvg>hxD$C8mWcZ8DHHD;3~W4VrGrnK*%bS9G`CRz&y7-?i1*aG?XO}98-GYRTFu5(a6Cp8jHB%@sVX(E4Uo-4zf0bppVkuAhRaVbHJ>1y40U5hd=4;`|E{~(UtnP$Za%!)=XNss|(Y6|ywP2Z%JOGI%<4x-!R+A5Q#$d=7k<HVq8OeKNPfM?V8y&OaHFWsH5u<WV4#|6#}EGLNW5HV{>smjvZr7qF9Khz7^G#YFg^5VZeIT{tXJj1*vTkB;In2M>lyap^or7lXeG)ju<RuT9GR=FUwSxUCshTmy)!sJXrzp_zsHKxvD2el}OoLBZH6CDzmBZMgp5<#Ah2qo+NDz|Q(NJ(D^1TXq><=%9u1OUBGo3-J1%A`S2&(r}3WwUmxJxohF%@Jy%T8_Dxs;U8*0W_&?4$-4xxQ1%?n(1aG6<g;GIzl*FD)a;*txR>cT*>6=nOJ9s2zq#0zt9J!<X;!9o^yo>^2YpV*7c;0#F=LdfZ*Kj=q47^tJP@>2noVhZn9RyZWre`KXZnWtf{Lgg?WggSSW@{X{t-7K4+0AH!5^$St2vN<dMI$5bldoo!5fDv=?bAX2`TYnh49AsS4H3ypX3XNVe&onb$)?ZB$MQu_s6tz(7Vl#3Y4#B7|E3q6%F%I4j9Pv@R31;Bh(<?bq~&q$7<MyG<b&aiO1L2~e@FEo;R%%sv_r@%bGH`&irm6a{V;->9T3N!5Nl$^G-LGIO)HmD_^b6g4HRgbu9;w9jsv5Dt=tsYNjITLYFd=ftb42BkbgW2;7oD^Cf+tX#VesDGsfN_umyEG?Z~M=u-r`8f8LMG`t{qx*eMxeaV->^Dh?cFd0$byAM<A(-JR@RiMq<{)O2or$!tl+34cdMI7Y*vg*2Y|60bIo<$bS=20z@3&b7yiX6)UlP4AlD#Fgb|;FjZ{3FQ+mYtkW>Dbl2LN7Zy()1RWM2T*%fgJBQL(AYrb%8E_B2>eg`=1)k17?Vj?!HM9opH0$TDH2t?ayNbQOptIM<O-Q);?J1(^_Om`Y&fsYY|t?hv78aatEwF4Dqkta<ZtNeYZ_ALZ4}szUS*J*gy#9qrcfcOjN^Y4q<J1&tOMY85mBVn>!DQm0u&hdESZ`pi{FQhg-+{vX3dZFPMl+Yc}BZ42yKa7>{9H3CcE;LU&xpMx_a^I$6~!L&1}+mb;>)=p%qDv|;{Knh3@6ga3eV>7VS4%rAL%u@KZV{$bK8A8!@1X%<+$@22P9tgK-t&o4Lh&qc*lITQ*oiIjc%viYb6YUz`>`u@n4ay~@n5=*cNuQA?DZ1kjS-sCLZ3^eplqPgq@>&_%jhLCrz#Kr7=do=TDysy`Q~eX@h7=pz7KO3hEnaI*PpRp6T`e;rF>{4KT`4pt1<tfCN~+ikuuJz~a*ibA;C6+E7^9jJoI5Q=Wc=c?X_D1<72J#_PzGNd^8QuZRJW&?b6wQLW$0bNAW+&(I{r|l$kQ+z;8o8IWMM}%0_|3l_qNEBNA0BKZ)A_aYas@;Z``Fe_!pJ!#tEaAS~o<fA`%kHu>8_CMHeOVdVCdNW&<D}0j;9ACvSRYqI~2Ge%t_*>dmQ6af4SXqG|bAz^mK*4jY<^IJ2+X*X@h4wW=EQd$}|(yfl$nqQ<#E$S}FdZC+NftO6p)d1b8DM9Ta&ETguFvX2gN>9`tKuQ-DjyO<rGxY&8BNOU522@n|=%%md(BkV7g3-EfLGX2h_m9?_jjId#ZDje5RkoU?Ui_PWC>S_@{s*HV7_%*^$tu?C5O5~b7f}G<WXdlTcAALK)byTM$;grD|pjhQlyMzigb3tIqr^PuroQjQ5;4EjxCV*TqFf1CoWTn_CB@T9`TJtq&T~1sTfh(`HNW_kh(^<9AM$jNbH{giqMT(4uX>xh*oud_CO)1;VmiewY-XP9QOdzWx&t5_vI)G#*!C!aw5a=}*-&9NHc2JAdW90O<SPNMk{_z<yS83?<08I??eX3A^Q3{^UMD7p+YL4)6lPg8!gqmHa3f!9(eW+L71yq<fj{cY_(^GR1ngB|-q~BBgA0m4s$s8Jy_>$?K$3y!{v5u>#n+FY9mEg?)4Op~k*lx_~oNePZ)1D}eHdUphT8FJhBk%kc4?>g1_@_pejl?{K8)U<&@v2#gFSwLBrU*O^rm3CjRjAn=dTQ@g>lsn)*95;N9>X)&ApHcw{6u*p`lAQ|gZJa_EG4HxPhnB#=5n6+O_Z0wRgIH|ZH2M~aD_g2mNROl82`%5dDIdqk|wA67F}1!aeEistacPam;9#M`PFtU3qI3?E*D|9!XLcCv`6`tZsixmpf@GNV3tSl+?WLDKtX3fL7DIqC0Km}BF%4&A@5-dD}#lKY(kItJUC-Bu$qfWnK~}J^UW8iYyvl#NWxN+(U`+`KITvuJP_xiLuYdoOhGFN*lvMc5VP@?zi{(;U0Wr@-RkC8;nGsS0gT;O<$G?uU0HQu<}i4;TMAwLx;w)Lv-z!EgCgytz+KuB4P|^4cc2K4Z0m9k)?=f=iMTEX^@{J>lc@IfO`ZHnfkePSzVN?lb^9!UliWbD8=6`;#D~q#bpXZ4Bdw~XC<I3Z)vypf#uO&-PZ?>D*O)M$4z=!BTDGH85sA(qa$>(*{U=?Y;A}xMP9DL==>YFvdw0(!47BDM?Z*oyy5O*_B4Wc6Feef-fPlr0s(Rya<5cV($l1_$iANlNxiX)jQ%$rM#>~M4>slk^a}l$XF%r{OHkWpFHU+FgDZ-LZj1Hd8wBr2YvS<I9o;uG!%=;n=dz>Sp<fs1!2r?}|')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
