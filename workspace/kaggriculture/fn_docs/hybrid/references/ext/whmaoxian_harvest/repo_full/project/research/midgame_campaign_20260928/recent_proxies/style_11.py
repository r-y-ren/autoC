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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rk<!ERhha{L#bc^Ec1vc@;9)H@@rW++h9Hr4}SFo4%EV5|>g-;Dit%Obn`^~=bJ$gFBoWBa5AN%gB&l~t7)85#NWe_i~`ufP56ufJXV<IflGUw!y+@#*s7Uw{4gfBuipKluFdZ@>QbZ-4#I&!2z3_`}D){POCjw?DpmcX4^~`gV75dG+b?;m7aqZr^--egFCAyC1f%KL7je{x^sJ@ZpE;_Wk0&6n^pP@0TZ|eEa%OAKx#=kc{`k_T9VVh`xOP4{z_b7ve+mnh(EU4do9X-@beE%japk|M=y9A4akm<?{Xb504MSfA?i|_&ctr>fNi?TQpNYU;K1?cmKne7e=3U+Yk54AIX`8R*)~<;~!j~4C(OD_0uooOeZ7rhVlB<dbQ%$@276L0>|Mz?i4bL58LgV&;R|$?YrBbE-p9z96i4L(v-kZ9$x`X+QSDuqSbT%_&>isd2W10oF+JNKiwamb25(A6SuF{Z~Ec(V=%?F4deOPy}IAtk+;rfd;c7`Gghxs*dfM~<9r`i@Zn{aPl-d>|K#EO>+8Lr>r+EZ-*@%6(@}bpf2~dZ_?`55gQgyzyI9wmbMLQxd`5V@J@co>^G2V3i&@{FYsVk0O}@O!Yp-JQ6!2>C=pUVI@_c4)>9kK606OQwqS`ZVJTSW@&OFh?hN0IHCwS6Y9t<w{Pz7TJPn!C@*$48quW#SI+rGa4<&WFD`?v4j{?nInCH`>c^RB+~&E4&LcsQbO)3+%y;l~4NG3b?h4n3uKkkOatCzrkq;kV--lP`|5dEEOC{*U3nZj>LrNuKcVbZ_##C&!!X@eOM$9WQCaNk5z>55JoETB+eW#sfTOY&-Is;yXY3$Z!*C8$SGR;*?v9!2`FW3CIH+L^siv3$`SeBK77=gRI<9aS<O!Wt`_E2phj*{{R2B?#(8S1TV;a=(;+lY+NRMDp@ge{*oh$;XiaIRxjt}hvNk%Pt1rR6z=UMj&eA|EX1pP%loScr`HH!%_nw_=)>Hs5Bkf>H5tE`fml|Edpbo4c)K3P<2R!#=!h{Lhc@L+!G`l*RS({YAe})|B<%1tKfJp8b7$cE+Yeua0^`FYQ?KR2{oSkGAGUXQfAQ9P`4WdaV{zz&NOJLj<|x4X1LzctWi{C~+W^?<{t*WQKTdRvM^;Zb&Ko>;4&Qz7cf!K5>m1Crc+TOVTP|o8RSEC{%pN#LSDu{pV)2SPd<#e@MDPMUVHEcw2uWqhK*RxeQ8eq{1731^=l{cy-<N_a{}=td<By)u(K|eyIeJg+)?KySI^;~4PLlD!=<IQm$!=(U0fH+CTzv5O8}R?YK$!oBJQ95}azE|#syaC<AFhTjHW34;<;@sjv(~5&c5!@)x}vJC5poTqcM<2x0vxN}V)WB?!FgPpOBrB;u2pp3=%p%cN4Z!iC*<7S)*E8?be;4ZavFd?a{NN*^!w-<T%eHOI+<Byvtsh7ZLX&az9!1$p1yW5gvh-uAJ#+*6V{@!C?MmQ<>tOlH*p3|2zG5w=_<im7LMV%mS2IBSx5+;&D}h&;~C!dOvqwR519rr(lvEFPJ%Zcj~ZpNXLCb67!urq%HTS)e>{v=$+#=%=M`ZB&#gq?y}Yxfcf)eHhpP&`%fYIpgG^o3m`XT&@#;hE2?QrhoxlVKJA-!|eN^B)9z)6f93kJmovNqd0+=KJ9vYh)%NZ&7@6ZQ@el2m<q>-yALHW8Rhwl9I>wA6i&PVv{zynAK<WDAzx+?+EGXtv6kw{-(Z#UyuE6Za)HP%X4o==Fh9%p1W)VeyuM!Z~3Xi9y9%tb1)0wMn!*)#b?9_iE#3t^)94YGEo8ipJwQsmO8;I7t-kie<5W-QIJivK!}4k18Bzc$&6q-M-xN?w=TFW?O4hwrBA%&YTteZ|!lHBu)IXFvgpjEjeyR4`vdm={Y_H@=wq)jq1|jX0&(&l~dkVPDCZ^W6LN5`)h7hOOvfAPo@IcmFsVpTZf}8Dhm?%}(*aN!rbXMa4x@7*KSkmPBydomjp^aX?3B|MvFtKQH$8%jan4jZ-xOP{0+ip^(ruROyWF0NH(id;4Ll;{X2*zbgh9hyApiAaIGrB|-_R6``RF$7E>>RtQlGWs>MT$Ml<qr`;|c?>@kUuWv(g9uQ68xj1ENGWK2ET3JALG%XMwE$t3qp5U~g$%`gNx-RN>wpNU)595jGXfnBglmd2>zXX><Bn?m&jgANDq@(QB!cXz-Y!tyg*+J0r%K&|BaQT_n*&ksCaHeV~{mN`9W-D}s;`vPpfJo2*M;0fI$48CEUh6pG)!__>9Ze~o5apw*^a=|34_+i3zA`w52*}l&mOG&5%B2d|!Jj2xs6+$$Hf1XKtV|ERm&{7al+c=3p3Q0`p6BjGurNRws#r*Y`41xU)ifS|5sR2|e4vE7BiMq?3c&h1D3H6<$2Ap;ZvZjF+%%`2VP|AX=b$$Q$%u0&+j5PC(gzr%ydb|Rhc7TBffs~G;#HDv5L=2lJ`i8X=dENBI;;brs#lEH+1ZrS;$VPSPx7#Iddww(n7Xo(rf!Bb!^4cZ?n*Mql`}UZMW%>fX?~7VoVs-)IxBk_rASK4cT?Dz;MpLAfGcROkU^9r^~`Ddc%#k;eGQt7z#0^-M`9AOXqL24_Y&Wm!9FR<*rfS^dhoc~;JPmo1N_yM$7J;V3K;|@Sq6NWNUSY*zF@YY4y54hf=4%M(hyimJYN4T!ODUw&v}-a)3*d4iGP}=3M;gNq56{A2>f^od;osIh7PJ3s6d1>tU0f>vgl2{TyRI(4y0ngf&_6)f$|%eU&~IhFURD5eEaTCj}a3buk_>_Nn~&b(}b1pnRVhjnRq_l-FDS_^5aCLL|%F^uv7sma6zQE1-5xw<n80TZe|^1YuUutd5OqTP+kyu1xJ>;F!?k*peeMtk&k0$YrvRbioS>ZAYS&>PY|e_PAaA@POccDMT8$o8_NY0WQ3~rWt~*O^$Tcz6NN`o^;hNyElF`uzR&fS@&v+M+6K{0jJVWt&7&2u#2LiUSv8v{w&Np9XtoXMF1wO-Xc0UWFd;M{?`@{F1=XkLz7d`6f)cnm%Y;0OlbRysCK1;_uO$wjVY~NWnUtH9>%FALHL6nX3DKZaqH$X>^Oz?vAJ2V$wxgf1BXitL;@O_G`oP*}c%;CQ-dR>Ma!CnqhY}vmgM?%c=N%;R_@JaRG(5dpQ&srbJc2(ug8u0=l8RIv^3r>SqNUD<G6ba0Ir$aW&rI95Qo#8S0SuqQ9>#)y>!)Ew0YG$Pb)~{hL7k#k2|&Vs?8_+*wdOnD6bJ*J;Ji|GjtJf{Es_Bkg}R0tSL|bJmed-9itNCMY%X-{>T3nB#YXIDPcW0=hAqZeF|)fu-I&y*ZmJ|zFvH`p!rf7a|CN^l7-9&WfmH&;*k~(|o@>6)y*V&5l&c*NwEUemEs62^d#oZLm9ht~%~0Bj?iLDsU{NIrcMoGuyEe}4*hect)*J)PIbFyt&TsMuRu;wR^p}P^Q$N>SW-c=U`CoE+b^R5T7zU}@K#n>K)z@Y<*J$JIu?%AiS(X*TIO#Z8&BdFy-{WE>9<{ebQCgAhkb$09fk;^LO26KG127LId?L9A{6{+jR8bAG!tuxl%FFPkf}%99k}-tF<?J}#%2cG#R%z)vQ4s-;nqHcOD&^zl*}(<I<~jk8ZA8H=(I?b$$)Ug6_%Sg%E)K3Ya}#;FGKv2Cy2udLAPM{v>INaQI9&%HQuWvV1k;00d5?g4s=R!3mXhKIr`7pJv+$!NJoY?=`~y?zv>1^Ln-Wu8NGmcoFup3bqla?u7i<%ks6@aE1`7eMOiXNYn<jXhz|L^k8-k^7bRqQ&UprRV1A9-4Y;js)C3e9q=i!iFTayOR3Yf6e#3Fbu!sA#`6W=5S`V-^nF_%{Txoop)%ZZ~Dqs{M&C14rXu{5K=zGLYRm>)nu!Fd$o*b5Ea7V<z3K_<t>3}uP04$%d&#vJ{?a$y9If17uL&(`jYXo>K^SPq+Ef>OY|Yf!ArkWrUx8Wva$i_Thx2Ei_7XaLpVUqYfwD{Hi%jwO*|>T)I(r7Cqzd#rbRdJRz~M?8$yH$}4>3Sl}K{vYQCk00LAW#@)TECBnoL~@grPcI_9$DeG!{~oDmMO8;@;R^(FR!igNnXW&LqAgcfXNOyKC-<8)p!I*qkp$beBY9s|CE40Cc^R;ZkQ#j&<uw}Tsa60P6T)niNcE~ASm~F&+C}ip?Uj?*>%>5T`Z%3_+4kB)9&I+OQtABQL)Xm|j|d3QyE_R}g+<ru_@}i?JK{)cZ6ON@YUXSmBy7SAo1`vyH=`cuS?Dss)i})Aa@|g`$EBwW;Elve3T0{{GzaVwWX(hliw2CAW7YNTd^ehb4AH`A$M_lY%3<@J+Ci?aiQ<w9e|(J#mjgaS!{H=$OL3cxw}Thx2>9L^8Z}AIfExAIfOB^BW^Z)=^BXRk_T8)+lxPaD74UKt@Lp3r(`ayQl;1_<z{YzZmt{Jd$k-nor2y`2XQSw|Dp!WStX#hemTSo8fsw&xVnpl`U0e(a@oFhUl)kuCmg_-e|2U?X_cvx8t6qL8G>M=cc|8q|Lc5WAvB!7MQ|yuXZayMFlQU%)0Mj&_xF2lw*u<2Te)zS6DjMK1e`vgRZNPezEW^%DlAXy(G?c(!stjo|2N>dB@T+!Hnw7F7HJfNRFn4eSyVYEC!eO=xe1g|rQB)10TsZXx$uG;#@TN4ny+kOY*_DbFz1ocJtlMOA&t@|4>wCP?X@nF6!_blO+T;sn4!!MmPVAuqHnmbrcYRv)TNf#srF1WC&?l(SGWE45U)%q1OJib6W;+VkP=`XbJtUXbrcnlPci{xY-=2BT)4~uc#jj2>4V6`2?f&-1SNFF=U0EYL<=`kP;AH<6kE2Kyx(N%jD4Mo(966XwCE|_2f_8aif=5Y3vVCm$OK@SR1(%cK#H0l}&=6)Yjh|Ac&CVGfxrlNfCYU_9V}N?Km}pMlSbrb1pD)aXmk}{M-a<k}1(Z-*f=7#^#qC_=a2FUqi?)XF6iQN!P7wmHs3I>0+s&&Zh}KVuYxi`VYT%4|{uNZ|oSioEt%Qa=^kHc!Sh6+OtBb)3$eH1zWLs}kSn?zRn=jxF5|ysDHXQ&OYCI5H|1D9G$&=3t6<L8lrE@mv3l7^<im9-34Lh)lYip2miod_Wmn!S?3Gg38mF&h62SA!~^i!aTixAhDHEi8Eesr%(1vz*WW^g(?g<6bpq|hdu$+8x>?t_~c!=s?kgZQG{XI&e_)PfJ>zABD0ixI#aJ0i|y*3@E8WjT6!+%SsYkk+LcwXyBVsS#;vd~0TCZ8I`o1!fujj2f&Jq2kPS@HpwPx1SRUWSmYZxJU%Ag{B??ZgJU_u25STTsHDZ?ByXUcr}QA?P6#Cf6@9)U<#EBfV>0q4ClOAw#f$Lbt_fan_bde7AB^HHz*|r5aE$b7Q%7~Ww0wfvL5m{;DD;4&jUipfUHMBfyt8|31y>49ghG)F9AjDPem`;7h(Alikwpd|BRQ7<tNAh0%3DU7%y7DKDzx~US)(N5?v&R-4e}^N(RmVlbXmO@x<^Q7KT-+4k-#$XAag9suVWWymA6SJLG8feT-XRXzi>xsv1EQJlVL9c<$2$Z!2`{UR-0-+cGx+z!`RTco5JCSHDt0B*cY=yHynKLqIali=zy%j5LxJ@DUHuHQ?Q8TWM6$FFz}c2cDqO!|L;UoX#6YLmDo0C?W6Jcnyz1%p9;Uh)^lJcc5~+BAN*{b0H}!4x>~Pcm`+68cFpbmyz&fFj{SEIgTg9-Key*GfTh#Rk;bJA&^Sm0*k_HFOuMG6i1N?7I2hHx?ITY-z<KRbwn?9xkY(_$d`j9Kys>YhEaiqUjI|egq}mV;_$=e33HQ((TBf@$KQ%$LjtZF%E|1My4Vpi;XSBGRQ=x98YuMpA{+?3AwV;Ec9GSX8KX>xI5_D5mY5n=B9Ec`YUvvq;lq}y#uNv~u6;@==oqF`TEZmql1r_X!RLe};Zew9;_+<_ijUC;Nwmn7*QcO}Ik=$QGZ<tHpa}p$ba!a6&_*}69jGhdv<OUeFtiuN1<)v{&sELzR)yu)eD>$hG+=ut8;iH2*Gda2dD?BTMRTSqgPj-I^eC9oOUi=FWWhZt-FcNRRPO_1`la@Z0HayhaT+_dL_w*_vFLtjtxvZ)0Up;<l_aU&q#6S(t?t9T4yVy<zQa_{r?wOI@CL4<O8!8y6mC8h6vj+hC=l4^_*0FS@Uo!Nk&(ejGZ<i`tFlB^6EVz4__8A3JqPx1e9Kw%gS3=V9-}Xtgbe5IU^VT8#$dw+w8E?(PtqID<SfuSW>1fQJpQl+8-!>g;}y=CbJoAX>We5EXNYDqx}8J0Wd^hgzwE-~kd&6eAwV?MVZmaFDWA0t3{i=`Hlu53d!ZFMGjKlw7&rokLN5-yio6~+tzHg20T@QQjHIQ757(A1XxI0vjV$Elm9QT(xO$&9++<^G2)u#01_y1Fz#?r~yjU)&Ybq8EbyS>0+hCEJcDL0{iCb@%-Vt94#lpN0$sG7LEtH`F3>Y+=Th>SlG%C$&?5VwxEkl#}RCpy)c3~BKc<cHi^oU~|k>s}ut6+5)&?T03PF#avLk5MI3TZVNd!Y*N(}E+9$JZ5V<a($?!`7ZjN+{K;CXV-H$^4?T#-3i@EfWdsa8!r)U*zRyVCtAo2Ap3av*TkuL^qy-PxP14F^n&*kf4_pu}F`R^EHTJ^t#s~Yz?zXTulsx3HbsU`{vq<LR>-_X)!R&VwUT!e1?*ca7!?J;>#1rYCyM(x-2^)qt{`y%+u2V2Z?UWA##|qP=hGD3t3CERHV=7Alp${HJDR4N=8eU%ZnON<S0`ip0i2v^~H5UeiG%leQC<l2Ag8)Ru!Fln*VkU8K?J;RP)%SzCO&|ZVS;DWW-I?JuwVRg-nzM^jh{%N)}VW^p~I|2VD<1y>cX0Mp6+5iSsZGyQE7}(9scn4G1%y)j<uF?NvK}uvYeD&-j&7=hDsSF%|`htPYD+RWw9a1)jg2isGE(v?k(E?_#8}c`&0C;f(YNm5@S)(dtj@iu$sfiHd7Lbg6QP(?RoYxQ<{hhA>(R9|n^~Z+XC%As^7|q;-nRv2K26fXXnzW)hs@owo+Zrbn%bF()Zd>xgC1|J>t5*PCdn(+@JIEAWpBCM+m^y#TC%hwM7isfDH>NhxRTiD^c7qa+VfnRL6svPnlzC^U@*6T6%vW=fh%J@~2`EfBO$bZEF^<21woE=t!CiXc^1O2j8Poz^<<1#lU|a?3!9Igwo8f9)imk>7u8o~q9YbB{T}Sv~7rrQmIJu8$|Z(W$y-zSUoYWnz`?$KmOe*)DH;R@xGhotH!QMub%<S49wSyi>oE7C-E6Aa5XY-uO@g-(wz1FS?25BQNOf_l2xZrRA{e^KM4CE5ZoCCWyvmQN-{PPd<9%>VX?Dmku*(saTt<n%fXNYIhjmv|m}zws3fj!SqO5e%uZkkBZPtbn=W=9xt21z+MFtQ*=kb$m;KvY_{VjG1Fn4Q9w=<1WiX6-fN$d;xP`C#QUbXqLjxQIv_MVJ@8Ewh#3WEjxA-r#-1<N%^#jYapi`!sJ$AZ!jK9DlK`WT9FBQ-U7QFLCdQ25PHK{0(weB}>?lLZRcalC>ug7p@M0(8ee$NHZwz#pp(Ge4x58kkW)i#Fi-uBTT+O$$wJ9kOo)aMlCMpD7rEzdF<y~26QQ3f^S4vLI8^q3D?MaoFG2BhbELLcQ5{4W~?^qV)jY`>e@6{I;WCp>X!Iz9d0bO~ih%urps$?d%DX09hbm}<0K<mw|vTa|%Ew%6tyMkI0x~K^x2Pm0)VX7C^;TTu|EEuxJTotMvR@-7i;~GJ&Yb1(b1Y0r~feSpGVU)zkZfT?O9S7)Vb~x%81kWA-!)dn#W?f%7lbdjDl=_V;b97THl>;DQZ9r6*r=Z6|<*P+HKRa-EVYoN9Sqd7Q#g2Z=*U&uI$4oZqU!qAKrMfJT5^(d}6q?@<vDt3r38lIWGhB$;EJu0@!P|3zBEBbRshG^eLYll5Kao*CtOo!R&ky9Rfo9xWvS(w~bt_j!_ia@iP^n~IFSH#EP{0yLz(~uLnh3%atqCAd+i12eIc-hANFm0ey^P>;?BRlP<JCFGtzF)t+xAw<G-lOgz}QOU#E5{0(J`4fV{HY9R;{}|AkOL%9mof89gxF>3lYaeMT#BnUtg{>IYUj=6(WAVplEeB`02cVK3VQ=@4ZlmNi?#!9lGJ(7KSH(*Zg_9D+a|2sT-mHs&7@Z6eYvm3HLUoUyd?MAW%+)MueVcS(+i>c#lsPlbFTdxk}#QtrRiJ;*S)iQ{vpht3PGfEe-<%BiJmv@ua(7P>oc#-c~73jqGwWjCDLj@|$PCI$-|QhczOVF+dPchH^Zf#qaNK-+X+1e?sz^p)GnUuW~Ig2Lzj)QB;Mf#9{f|TvCNr^VPbVHa&JbgwL`}R^d|ZhK#gCrimg#wyszULOYBUtZYCc86r=@2~pS)4UIWJq>48Ry9KFo0G9zHNb<ln_Hfe3z(fyeRfbgvKPCfFK@$OoN%uQNe(Q`bCtRj64d)7Q!qip_iOu=lLz<W}l{8>1WTqhjj##N0xG81KY~0l$ONE#0R6Ax@TE3oI`N$JcD;7M81U^fe`~9KCDKx62Q$7pD4R014-Bfn8fXwiviIXquP_z)A)BVk}^!4&rxo=njF2Dzrt!CrkKKwX4Q=}>>u`oFgREeQeY!VoBSf?g5mtob`!g;IJn(U$4n<P5C{#39R)`Fhl4N*+Sk^y-!j2i6U{y8`jX$|9b6F{iZBFOn#!3#`!1na89=?1p$MpsRv*h|N+BB4~Uv-Og-i!A)?K2V)172Y=_RN=)DTrUF=K#Q;kSgEXN#V?Nb4&qz24Es?Dktc#9bp5(|lUPS}(DxaXG)qf&kI<S5A{acK9U%KAl7r|DF2zX&?waJ}6{EDW*1&nIF!o^%g(@nnawldhRG8mo(R9q!WJL3$vUp}Y-CYZe=J+_A$zg#c4<Jgt9%clVv5vZ2S>Rl4$3mPmh!gC&QWv1ykSuHCyLR5;v$NWXl~Av^G3$~Etn(Y}ZWE+Lvba9sUr61V=Go305j%uQ7Z+{yPr95TUrNK(^q3YanTCa<<sUhlz^hn+x3I;9o2EQW?9A2fk2d(oDaiH<)o<+{{oDbLU>-BD>W1#2JWNs~yMaa9p)vuH@h%>ZQy1Zh<s4S$oCxRWvMLseF%0X)d<MyLVnMSwB-488bPHpifEU6q!+ByOn~M9f{{E|B%*ahX*8`hT&Im@>{Y2Dw!VL9ujZLq~!Rh1z=W(}b$KqBFU-{q_?2Y&hawW5Fgt8T1C!NbTKKUSS*rGi~un!8y2c`{JMkMaWae-<(9gx9G1Z#n_2%JE+sV2A5uv^FL1b(Z12<1t%AW3*hOcO=2YV2K%;Burgf>&&lO4%_vqPDNj1CDsb7+NIJTWNN*H_t1_$W^<a_)<?1o5pyKH^VZZgGr689EnnV)PsW)*%)UUbTAo$ame)3TBmt^XsBcI8ETj!NX(BOUNcmyV!~19&MUmJ+AdI8tlgBJ#K<Z|bLZUS_ZqD<&uGxIJQo4M^O>r=mdP@k*gOXZ%2(eQ6_8PXm1(o4l5+76j8dE%DLdQ7QJzD<wcL_;lY%Z)xz<8G&H`N&`mDkQUVw~iSLzf~`L?8LI;n^8rgl8R^#Wl%`m@9%qi}wu_n6O+aIqD1Jym!u^STuiQitT`d&v=A=~AYg%O2M%ej4DVKY?5$l<`uk9A;b9hIy0}p-m-Eggi7MD!bu%4)nRdX+)xlQBzK{Y)476bYA<@T~&T(2oF$dsIZ8DvOUZ$aZQ`z#gAT9iPt8$DKdi_Cx)8^i}fOrz%4KMns`X3eVw!W4`BTUvOgma4QEIuXy{2?!f2X(P|$8NdqN04L!9?7F@JfkQG=yinbaJL-RLMkK2@s6Yr-ZJfvMaIA;>Vjmb!SWCkT@rZZt)p9F&#UAY#aBm0xycOHP8<8F+;_4eKjQG978xlBe3Hw8^pLh|7(Ofu9R6P8*Y<DSNO8l*@vM6!Gs5KdLtS$-uCMc*!Xia~TL3zh`vjDOoOMWt3_~Q=iGAa8*^F!qA%;7=|f#QYyZoB6Hh;Ho`XG!k`LPq^JVSvEIiFYLR2eA`X%+8}#ZG&Q*})+*;5a@$+WZ2qE%PXe4E5#A<oV2_0Tw@=>mgYE_f6D16=9NIzkQu3~sgN|=R$Qu1vxiHQPQjR}N3@kVj3(CxV5n>(q&t#w2$EAJ>RO+`-9Tp!V)Xu^*4(GJRAx3oNV*2{L9A-6QE?d~IX8C;`!^>VytMs}2Qhs<nm+pZKc+h#DY3R`*-ovVXaMKuFtj^rHRuuc}b)4*9IR_I|ctr~=@tWoxCnthUJs1Bh=>vQ~ERKvk0R2M+VsIdGvjVaPg_-QOQK84``8-!PV+P$8*#o685FIA9Gl|lwQ9xbqh59=yYR52Ey&r55cqJj-?R^;kqhdQSd*l6D<=(4T|{mdm$0Vsj2KAXWKQ~qZm@4#X@{pzG0c1mvvOzA=!2I{nv2J3#K7`tG^%-i;bSe+OI^p5GF89N*Pq7hVq)M<*L#r5#{Bls`Rz<4P1VXkzom7=CLq$Jw0k>2B!N#Hv53#UDGd}lRJV(p1!X}fmID-C&Rv0Ut&z=+hWhbKQVJn;`ETT<>h<)*+D>fr=5OUI!FLBicuMMM_{Zp>Dz-Ec|kjg~I54rky$X1W8@wYiE&(TRuZZ(vg%XCS$Z`1+ta@+5R;nOveZT}#?4zQDqY!xghEoD5isI`nr;33t4ua6!h}G%-T#NXnEBZ;K2X+(|U-W@Cx1SI%0jLT6Fm@3gsje(bQL{<}|w#+ANl(2}=~e83omNw~Y5XX-808Xl?)xX7qUMBGFfd<wbL7%2z*q$-w2O@eZHnFo|ZqyiU=?U8P}8<^an$aV;CD3Zr;^_X-xzd9is2w$WZID&F^3<^}LHe=;hjPS55k4-5)MK{(ixFT>ZrN2QJfWvDlyzVx$W-SGEP)O>UX(t)hj9b)QNmgRz6d^TM9=c(v8x}#Dn^F$Aw%jG6yWcZOZLk@%e@0f~qBgFt<R~|#*pi?TS{T|cKY{ukpJF$vTtuCcg>@aC;GB5qjU8Frv~A@<8|x%PCsLpX5jzw_OOk++ni-Mdv|4*JAjMM}cYNlVY9X}Mh)Ff4jDU6n(@jAnBs+<B1S7-tZJmlDbvx>(D+v%^A9yC|6x|`xL*xpsDN}1!uj@j7byrU=<uUkqQ5r-M%4$1<YpKpi)zn}WmA=$PayG*2k;*Njsr7G%j<m36L33GvAfj|VP8b&hB6?F%btSI_8!*uhxh6NU96X_lIbPjcwW~8x%F*vg)trE79NrIrq}7)>qC`Pp*kBU5M4QEp{d_bVS1Gp$6`X@~b7ErE{#teRj9-yp_0uY<Z6`cWFXvromaJn93TX_IV~Px=s-6m%8!4<&YH#H^vsL~8$Y2#9q3m*~;F4XjfgSInsVgMr+W>1iCj;9G-@LD53=3Pdl86wDC>A2u^oa_!E-Hvj+Y}F!v5K~`Iqgm;0iB|5B|o&Bv2)dLi->4dz1Qj1mQ5HJ2G~yP?JJHQ9{6}tK34sKkve5$|D88r3M3VHq)35<sWA*Kdr9_4ggmSd49}*gvKhodzjo1u$1j(=hzX@B&cZ4>HHV#}Y2k=J%n(-#^2AoHT9dk-2Q87K8nMQP@jH<3qr}p*a@7>A_Ll_!GiuhD+L!|Ez#dzWK+^VoYGR4RZfev#6vztb@*<x20s4eq)1?z$Mu{oJr|Rk%cpj>c6?5iupP$~bSKsuGHP{|3Tn0LbvIa}(JAUDKF?g#u=f0<Hs^ZsM78U+evuU(1-;%91yT9up6<B$#x3L}U_uxy^@RgQHo2?}-I8oh4m61uLN9^|YREeTbxA1=LV%58xP-sakql%yShH&PqfW(R3)wH5khZc;LCXp4<&ao7J3FS@7S~DfhyGbaJh*YO*z02kLHmOznn~+NkaFqL98rF+Xg^VPvF#_X@V=uxIGzmeg_(@#I-)9}WHX`jS9cklsyL*3~Rd9iLkqq>xWuo)BG>Cm18+wJ9c+S@Sl2ppjSQ|woH!>oLV+M5!Y|>F6zRvTOPAg^O#<a)Tjvv4_fOck96<vMvO=jsQzc~bVCqMnNHm5&2Mn~`u<s6V#k2Wa(m|5QDCfqg7t1Q>_1xw1GHf;Iy_fP)~$0=0^')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
