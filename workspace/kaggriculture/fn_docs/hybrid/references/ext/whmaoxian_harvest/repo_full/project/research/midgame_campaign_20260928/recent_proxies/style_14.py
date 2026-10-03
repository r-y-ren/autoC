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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rk<%Z^-Ea{L#rxv*hv#=DkOV-eFL35s;V76f4ck72+VFUH;({&#c8?pwERMn*=S_ifFtQC-jT$Y*54&;R@C-~afRKmX}3um17pSJ%r=A7B0Q`qh8@@xT7<zdt|l`OiQ9@h|`Rr~mo<_s_4s{q!%tKD>SN<HO^t*RQ^NcYXEx?|*sS=;0sUe7L;Af84#|rynkt_s7@ZXZ-SiulK+0?Yj>jf7t)HpI^Oy^W7gly+6DwfAIE=j}O_kdjH|w_n*G|`1vW<A1)6ccMI@h{u8h9x1ZiTe*f$Hho3%vdfKgR;hx^*o4-Ez{L1Guc)yxIT^=8IANzOD-{_~y<@?W%|9E+P_jdP1#fOCh^7!!G<!}_9?#S+srx)4-@brOCU;7^p-(!3D@I5|%=-d0{M@RN{5P$#Ix4Zj7>}Vc7?E3KW^5OnR-?rlRm)%A1ql*p$SmEc#Za>kUiOia9>ta{x@P%><WxwZ7?>;>(nEgWAf60ej9`5b$eha?;@b3NBFaPvS=(qRp48GsFXE%ADqAi5R<M!YC9Z^kk&!s9~5PagktkK@GZRZ006Pl(8doBOy=Nq)&`|Z4c_wZyjZV!FEG1E`}aqBL}d(028F}W!lK~Kfg(<d5>-p8%Ro!$=8Z3~d;4h>82C8(Rdd5zoG2|b=YV%tt1V=2k?fQyF~V!MLqpOtQU`|)T&;$I+!GMT$Z?(ywAvd}eNWb{7UPL@Or;20d=nY`b3?;am7-+lb`_m>YJ-#otg*ZUQ{KlfhFW;gxI-Pyh6>)-wEcX(Op?rb(-|5oJ&#s3fgK_IY2Yn{$>Qd@yPQ%X+aLkT|`?$Y4{`P~nX!S3RlnBDnKt&T}6FC_-M_G|<;0aypLB4h)eRuUvIW=j(54@^|B{!Vt@JbX5`o97OjXWP~{G?sQnjeFex%G<W?V|KU$^~;%ixNWc-SiWtM62{Oj^*-q{ORf2nqrv_9y^t@x#Ua~$NPKzgq_+cbI}_5X=%ujmxA{@$YY-QwBVJa@;AN8Imne&V;Hj`bv?>M!?}t9tJeK-Jx5a`xcKj>#OVF0w&b+=xG$I14bo{jXkl77Q3fBWBBYHNKOdJvce~SR!3v8dP5|7JC#78{UU9V<J1XdMHfCKKkm}rr<wOFbUhu)_w@!5HL8nZjg(|-l#7rUd}E?hWZJLs8Pc`<;A2Z7fuP!E#R<$r$HlLMXOp<FIn@zdBPaDYI!jJDE1^whQ5boZXZzvHF6e@W=sZ>#ac!-s!%<Nm|{x4#n$1+g3Dn+@<8QB|D;F{poZeg_ofW-OY)rvaoqxs_YA#j1qq`xU{rVssO-Z5#_S9h8=Xh~ukON!2HQ`uO4D`t9YzhkpUz?zX0UM?iE?)Q&pBQQ)d<&cg1vb*NRaB?%*OK+8bW2kUQqcggPvD{;3E-il+SgO@Cb*uvHGtM88ztl;`bCRKt#UeRKSwu6!aUBG*xnQ^-lpqi*&>UdqK?YL{7e>tO1AM@N#0MBe#-n3;mluXzI0zw0PymEbKT0KJHNXg>c9|2mwrh1t9jJj$Pi!#dU^JPhMK@ma^6K<(QQCVzeH4JWAbz!2Y<TJMUO1cKlxA!p>Lw`rNDhui{1V43VJ)rmplZJQLlC1!zc)!~jkBEPoP3HkFJiyHI4&NZ4&06CN9F@UPHg{QbKCGcx5ovvcujEF@WdYvBZ-5^|o0J3HFPNPQ0MTpw^~rq)m%<wgDC;((GW7;lj^5YaW&|<-HC$4&EIMg6*8+&^MzJMK&bB{pn-Xrj{nE!5<IZ!@cSax$l-ZQrHM-Xc2q(x#l*FL4(Qj{*n|>#gD6i(&HmyMyCQNnoEQrBJSO-~zV75<}Xgm8@<CqyfB#x%mGJKuJAuk!|SMNJn7P^q5TdwoV=_Df9mEz>}rj~fUb?cCzvC1t7wpa){y9ML5a1S=IDrqJEqGKT8>q^?YVG>)__LWjz6yAWo6$_@ucKs*#NuJ~a2k4bJWrKC1B0{3q6|~zBM3+4=mEnNU7`7>c)^&Y{s<lHU2voUMgY$&Aty7mf+fcxkHAt%XnkD_I$_lA@pqy{ZXpeQB(&W{4+bXftwC@N`#qC43pLF;mS42YZ3<^}+Lwex{<c4giY{T#PQwymj$P5%{c$ZZP0F;QN84ohch+RXDJ*dM5kZhjLQn+y4vI%d$n_fEp&6%I7Yb4G3lXg*@^h%n(Z99;wj8mpdJyRm89-J8I;Q@82&RTZpktIb(lu#i>HJ)Z&;8n^G0OysfcZF4+Q<iT8LY_<H)q>jpEVy*(xzJC6hQUnr0@>0U;wu-}FutJEtWNR#HFzKdW;!+-XZNC`R~>s;X<t<sE^h)?O<)yiXZyxA@er`_fsfb@0Qjvw_dwA>=v&4cdw{Yu8Fa2Y%tEy`FKGDcM*|KK(6JyyFjp};0N@9-1|2Tiv7&?U2ndM+K0aJM0yd&;cnT-e5gYJyxyzU&H6r5yZfQF=CqPHS-Q}yUw8a&o+)A;Lo05+hjKHX!II>_qwLM-$wsmt{Iv_)&v%9VByLXR!U-J0y_WM^a9nMKwhI`i*t-tCIGwbj5R1~HsHY(Kgf5${1w0}0>X28qbxP}KY>G8u$BfXKGG7^A@RB^Bh)UTj1am4j@E(v3IbS|5MbJkosQ28)1Q*@H{1YBN8qU>npuU=UN+BPu#?vcQCd$0!RSRMwdmF58ZBAwjG3e`xEKZ11MW{o-M&$=|&3CwE@j_?>SgHyGDMu2dqX!311^UWfu)CNlhY>E+NH;Bw(NYwjzcE+N^8GdklObCO79h@TVj*__sUK{|CnETDrqv}}VCiCVFipVeGRc#Xl(S`d|#06>hi8E<|qM`fEsz^rTtHKXdi%11*Z`s#sLat!zFANS-F%U_`NRZqDRWPW;mn6v;bdJxOvQw7*Qvd`}c1#fyWFgBQ@m=E|S{u;mod2kMQOJLxNfwk<!lU#>+=aF>1K?B?E@F7TUX(7u)u+GG=bn7PbFqJPQFp)|b8Uqt?cpwSLJK9~K=vR}Ik!h9D!{wg;U-2oD8<j&IbE3mMIX2HmJ`8gQG1i3cTpidq0}i#rZCH&p`x-^z@;v5z7qPvRjda#bGBhOkOtH;O&u6Pv@UoWwf%U+&U+CkFJ1&!jW7->vH8GK3b)5q;&T8`9H)xtg8C^`AskHOQn8g{nnAao6|=)bnf#ivw8X2YO*s<H5pnW1WzJ}A3`CpK7cFEqq2MaPdKUGMNK!?AzPe)t<y*=J&9<q{_!FIDWSNLt!CeZo)I@ZUCeLZcmvggwb2@4A#~uJ?OGyL|G&tKIH17fNaJf1ODZg!=H#wHxHV+$mf)hL_N%oHCfBpF8@ehEu(%ZEAUK?EhukR={J<o?G6zk+z5g=3gfDg*tRL3(BZqsRio^S&gQkE*f(NP7U!MO|Iv^gPg6^_f^cGWT<&D_H}s4yrc$pFLXxC7`Yze`7msf}6E18v!oV8Q;>!Z^U~uqmv-@`3qjz}nM?;({4DS=)D`*BgNG?lLcr^Thtk&fB;!?XoL54X3@yf+VU)dr>B^vutoLMp2=?Iv&c!VYKO4zzzX8JMsu#Yc4x3${p^7<tr+s_gWQ3sqR%lwKI~umM6%G;j$ZqOj&Cf@0vsyt?;6U#s;R3A{`ZC^2pRdndK|ZbL&mi>jLm=W0?2VXNw16jyA3gVv6R(s|8Aq1Mg+V_jr*MZDDE!@*=R_Z`Wu^SD+Bc6zzZvZfs^U^7~Q;NpNomuu4{tPjU^kb*IoJ65n4H%}$}NO@vz(EkMfn#R&Qs39$m3Q9;0vGeEZwqX82=!U}F*X)O1Rm5xG-Lm_>IQ#&ko5Q!-0TX+sP5T(2l?v?Pi-Kn>_f;XY6rOTZv3_-v{4?P~^ptZjl|1@`&p>(8(4M!**yl~7(>y|5n0S#N`A-P91)Eofg1rU4Bcy%c141n@N*sfibOtVZM5|@j%FSa$wk7r?R3Rnw}@QFRM7Mqmv(hc8A67G<-13?IDABrqfl;!2%JB`Xk!3*pDJxlNbY>BM~QmT86kGm{FZFnX6ENCc31(Ju0FRI98_h=J3j$}_F@e%~!L@k6h^Pn|)`pT50U#|JIYuSK}YnKcMFDw{01WOB!y*y!v-cF5`8rFX*N)|&J7R8~iuGdB#K;*f(Ggz$WJ*qjCVDXG^jwTZ0N*uEdnOa_IgN{~&N!e5ko#A4Pvr{|%-Btdo<4o!#*a(RG^y=E_jPd3&`9z>#En9Q(j7y{hry2>5C3ft|;$=;wt#t9jmt=EyDe;Ip8%)ajOk19x(D2BY3^e-AtI}KyAXO-7Fw)*DlTNFdrC)lwsxe8ULPHSvzO^YF+r=%V8fbhyfssCB{MsPxC|;B<X-md2vJqi)uG3vZG8}u3LmaJO@kp_{sD&$dPW5@JRqEVn%6k$%wbiPw0=1(Af0FJhfgf=)-L=Ep>I@_^y)M8|9KJ<R8{JOu%Q>ZzHtS$)1*sn8fTvttga5ZM0bix9U$e-<47eskdo3Ac=KHgrp6yyaQMRpo$`;gDwE^e=$%Klu=i*rCxLXWvcN-CkL_=)-D;k*=``Q8q=ai{Kql$1K2M9)hXeHj1d-iz3laz)l%V#W!lW|K7r;3ujZBq`w|8o`B!j**RRA>Cx)Zce&w9n%Rf+-1@`K{UzB4k0kpox-v=s!XrVBUp~FQ^UEt)jft$^?s*AE{MNe(Aleje6=U$LtXV#p`xNNY<U`GM|Q}q*Z9tGdJ!Xtq*wYB%1ZHU@M0I@y0F(nsfH_(IuD^-Z)%Ov6!DgB?-ulI%wZ4tjoBzBA}MG=bi@pAan&TgHQ%ln20-mw(-N#WxO-MuK1+GkyiM@a*VbYD^qS{#uLFBBQtKdE{r-Qp^ps8tRob1UG5UJ8G)Y_;Z^(<LY6XC;j#O;N&&$MZzFr1<&s^<Xe*Z?uU4vml+9ObjwU@X?nhl`khHEaDdK@tC+l0efjP_=;t*X1v_gn3@Zp32IPtYhB4&Gp`e|c9*)15DKq)s&k8H-)5_(x1u7|{#N{WdUipir|;+@+EnPMEnms}gPB~D@j;NlFtBNXgZsGC6duau{CF}RB)!IPJ?lO-v1&VH5jqPUi}@V|9bi+E;53^jeXvSfBHBSj^olFe^gdkzE3io1e%<U4}aJC>~rkGo{7(5xG2@6%1nIgSC<orX2g+JP?0h$bKIyw)AESXymoV4<?64~8YQy!ySISP^?daSn~yPCFR*UM?j|lW?cm1-1g28vGjG-VwRqN}#3sEqF@VKA({f@9I*y*&R0!3jrU(Fezwb5l=~7<TSMBRtkZ@=UMN01>>l+q^GkN4xWW>U(QfmhBf#`=oZ(E7?eG-SEtaIDX<$6ry6B<4M<=`SK+2{V>kth=y!~J7^<E?u@UUNiwM&*VRk#BaQU$nhlfMd?VSK*No0D0S#3>~6r4n>n9KW&)Dx7!H_v9#Eu$|u+F{^=NA)NpDJ`6GL0$-a+p+u(QTpgfO$s7Hb5!qq3R9rag7?J%<>dz)RLcOPc)EZI%sx<>mdHzr;ol?szA@Vwsl%{-I1Z)Rn-omikG<aD$f4`#Qr`F~GIy6A*;4+V=NlL40r3#i#4Jk$jpo29pST%%KPTuAs2C)3|D7QkW^&zYABSN{D(7~6u^=v@j4xujr<yBgm1%cyEpyW*dnNQ9;0hZmCx!0#ER+6VS~ea8$01F6n?{EDcR3&fSXI)@k@}x>gmn$x@@3vK*Pg@ij-i);<Z5hKuoV6h^l6IaikFZMiPFhv=!WHm>>jxR{vu+WePBr$JfwIHVhR^pN?E0mmaBGGA}_2r7HfT0TN@{%F#*CTnXqBA_wCWbT${?1d6D$8_j{$5Xd0=Xckm9YMB%b8!I#F0<C^jQ`@&^V2kKY1K*lOBmO4%$gN#Yt{f3CK3s}7y!Wq4x-QEeR4zX*Y&Vr>Ae*azo8By*o*j4I4meW+9WFVbaWNT;vS<-+`1Xc@xCui0G!41I{8CrXcjPd?1BF!E@aXhd53hnTHu;kkoLZ~Xv%|V92)C6cdi(gZoZH4XecMgcCurwJ*O00w6>Xw_z$qEc6Z3UKE+p{1)3|Q`T-eO<LrQ*u;G=JIPs?OT6JA?CY4Vr8l&}PGzzavfXf}wjsne*L8QksU4P!fBM4Rpaq+eIi<YZU)L)(j{6#Zb$=!v}_lQexCMnVaevjtZvsi^kpZy)))|!)&b166f|YGb_cr8ThfyhfOfUA;%W-s#pIy2C35$ynr-@I#>@M<SFq`M8;;)CC)Hx@OM3X75e7Cbl_g-5E=v!)TF1-wK!rI`*wYL2c>D_ol!*%NnWzrJ!1^Ui0p{9Wz>6m_uIw@{S-2oRKjh@`<!I1PF(P)9!vRqEb<26bU5-OTY_yqUU)Kn7%Sx+W@&f1*+mp(pwnL(15j>dS7ZNgr3fw#O%t+$2+9LhJiMM$Z++$UXp{ve6`e&LbU(oT2&P$wfOgk}_vmJgf%C&{QU)ob_n_BqIkel1F{=O%DiOEv88-_pF_)}kwX10{EI(a^tE-eh2-a>njH*KMp|Fq8uo~Vyp*M9br<Q9~uQ+@&=+>f{uUT$lXcsCcr>85y2@`m14zV>*<a8V$#yDxva1i{G61)ZxSxjf9sKS$A_rvvCf+OI=;=%Es0#aL}(w-@)LvAudc7?n#bmh*SIGKfsiR{^#4h=VQsG#oTC)Z1}j&&&bvQm*qla4rBO$dK{uQLlf_m1h~UL0?Hz~MQ+L9$HD*w^^$md9IvtgB23RaPDJuR5_frT3B8qBIT#7pWF|DcOte>{qI75aox8VZAd#2S!!OG_ok43MKx6Y$_{=3k|TVp0e(j_U}<x*TeVIr2I;tffNWT<41y4^+IiULcYeq%9LkQ>@u0hBn!LvifYt>pfk<sGNq8Lo#h;HwXX`-O2`t@1NRXW`kIoi+`$M5*Gk#yJUw=YcPy=Fh>J(!UD8dyt?p)vQ94c0F(k3xo8(T8uNBj7KeUGKOS#3r4OFA;0OOF7ZjtI;=Sev&A@Y@wGN#2^N_=B$fhQu#AE>=zoCFPvoR((|_6foLUse&T8E*uzeo@_u;%hEh98?jkwX;O@I#!LP&G5RQUWa|ipBm^AC$vE>^`=m{@|pMys|PS{l%q64Fb_vvOu7Lwv^-$jCIl6_KRM>0=jGro)o--zRm$ptJvpF$WFt5W#8uP#+PuOq)}jt1ny(8mv^~0nGx%*f4eMANr1o*~JUyG30vXDDz*AT1twQ_<OV-^%S5fd0z%*Zs)=O(vkB~twGDhIU!zr0Da<fBOou~jBs5r$nR><2fD@HBf(M`n0T__=}uSEb=G$UU<TlZqaogl0PCYy+-C78EbTlCI>k`t8NzGFD8K&?$^S|VB56HZbk7#!p&GJ?&cqlP}tul?NM0>m3}*Nid^I6PHp)z$)l?;_0fJ$2JnU>KK`ix4Su%|vVJjQn)W-P+pPe7Uv{)jBIKxStVq&CE)u{`I^o`!8hrCh^paG$YxjtGkkh)jDvNs2$*ijL)U|{oZ`jKwikaUmo|O$q8B5%eGKY&)71bslq}D9S$4t`^y?o#U(eXfH%CuA`eqlDZDh9(N8m^3pMY)nBb=^da}MijYzmtMRs>0g-y-w(MuL^0NEyj$gHnyOOh*j1>x0ZZRdEXj*po_GE$tCyU2}{SQjk!4{rsuuD`O%ouwI#3>v=(?#SK?Z{M_%g5{ICs7I|pE{OMe>HVEX02(KWa@%fPL|TB?SoItpG`;{C^`i8aa-9bCb&KCX-1`aSz=BC@O}mIAVQ9D%fm}hW@BV%i@+&24ke;9D#UU6w>-$x3sF4LGF}RwX1MAp#8hz56q9rKq!8O|;RAShqOLrmcKIvE~lNv?4^A`Z?d_3wI>v|@dsaAAg)HH-pMQjdGLX6uOjj3|aglo(-K3rmZUC)FvEQu-B@^p?v3H0(q1|YD+L80}~f6J+A449u&i7aAn-yA$TSXgvPUNK4t7LnB4?}f!F2^q3L3$W58NU0u>KX(J+NuueGWt_@EH7{*q5IXL-v+YN$F`E;_^}d|(n_k+}*w*lljt&7-0c{nGa<x`}qCZHkP8s#QC<C=P!AVJTt{a&68s&PL^#XMcKZ`#NmbgFCM^g}K4FO7x*LjYK>YnDvI?#{3hl3muIY}H(Jt@t`H*+HaBPw3l6LFy@$-n1ti7k%#jIn3SH>Rjyh=-IW<`g=;I8w9&`Z~#L0+u$V!g~n8EZA4?3yIt`5_8aKHh_H8QHsWnI@q*33U`Rnr-~v4*nUpEe6`}k4GeDF1l&AR2*#oAr*PECGp`i{D$`gv8te~@so=uHSp3O~ZCi?c8itkJ4e!PGOXRs}6M$4?IOCM)0Xe6GHvoGVI=t`+6rZRt<1AhG?2qJ;q5-D}WbqBQ;qzN3H?Yw;g;N2N2(co4^|%ch`;>(h>rp$*9SFEyL}C@$*IVAA)j=v#3(x`FJQ@axw0D4G;KVB{hs4cs8>Q@az${VvQ>S+cfdS_Af4e?(=0FgGW_*so!lAAXQYs8FyPX|JYc|7V<whg?y*&h^5NHoNilQP0@(B#jowLt!O?$Dc7V^kPu`s+Y{q0x}f&rm!xHsw?_s;<soHR8<=eRD?LII>3EFxD0p+uUHN9VFyQ*mg&9c5J<d(EW6V(eD)d%u#BJDmfjhp((y3N0(=KRTI2TSXETOf$;pTq=ZDW|8|8He1RF0!tAWi9M*A=KA0+xiVU{aC1@WX=ER~2!SJNu5$-@38rHXScP23eGkA`gQ!Tt)Ffn#7UI!Ks0w32okXv%2G2mTNb~q|t`e!3&$vNG_gq00=gyv6$F?hpM{bp2Ih9RRCI&QClD~=Dj|jsYQVW5pbWH+RojLn$um@E0)u2EWbj+BUfk+E}+N~EHp+_@Rl%>zTVTR}`%HT}ToM*V2cGM8ebcLQpYqt#$Lt9{$SsOB=L`=-hVl^9UzQPg8-yVp9PcNm(6D;9=&@c!$;dC>r%_m&hdUMs8aOx}``+LD&Bi|fz?3UlOx&IFUgh3M)4HiIGpOp^0JidEdL`r)W<SPinc-|qk_P2*P%Z02UIHBq0#m6J6&9S+QREb~;g5oplfLw%4>jbhPQn)hs4afPhr3#Y?U1rdatJ`{geX+-50gx#Qm?<<IDz`o1^vWs{M$Pq4c>2L;M0D2QNQ_xy7J)we_TY(x%$sC}^rpmQ7eRqGDLu0?$Y8Exjv~|myhWSnuJ~*>721Vs@K?h4A_4Dd0fpa!uBl&pcRw%@2eCgVC8XXQl&981H!edmzDvNc5AYuMs6@D`yv-0_9`=c96LR1r={xf_E3Gn~kk>AYf8w^m#*4lp8}_>eLg5QI%`$DxLNrbj&`pZVCIy8La5hwjM=Lr3h>eR`>V>npL-0Mn?O&hr@b=A*4`06050}gPyJsXD<9pPgC5qte5x|y3;|eGe*fwPQG36{E-D*XIbtsDWL1-jtf=4j$M#4j={4>RHRWJ`-FDj=^gar?La99Cxp78CbH;>={`u_8qe{$!l29p$ZqR=TGAav2l85MGY?c8$XaJw@{1Z^FNh&Xq_GB!#*5VK5?KExV^YNB?bWg37*rN9T-kQ%U>T&oy1Rsk8bh^e2<Q3fxL##>ATP>MQF;S)ynL;IQ_%;F$=4lo$aCP8(o%;xT)QH)l%*1SOBwCEH<6aIc(@ZqD*bBoDmoJ>Lcj<`lL!;X}ddj-Cd9(As~suu?YmgNq3m-%0ugEMKSIz>IxQV!O^juzX3$Wbj)OfkmZn<gZCJ!ne;ofhnHHx~{32dqjtbMh%x*~C!dARAT++4%m=KlwqvXZY*w7p<<8z-yKeR;c6?rK-vy;{fIQ3HYoI*<2%V<p8~f_D0O<>g_(L2!AFxXS=1qwjEVG@m9Ti_gGaRY>o@4@yTd8qq;biOEND!u5;}mdOv-bHmyAYVkh%<fJ_b?+af8K7DJD<O9w4Ar^*Jj8IhR~!uk<PyyNjLVjt&AkOEw#i>zjR^+6#h!MWC5plCW*l?ZCNGS|16gJ4dbiG4}LGZNomQ_k}4XgPRjt!Pc?B0(I&YMZqV@D$R_Q9U!a2+ic2N&y<sTKN<yPLh@(p7GzDKRu17$()Qk_)DM8o4#kXB}z3_E=O@Gv&ME-yDO7W6pS@q;DP_{qo*YIV-uK>xYv5jD*fw!7|LwcL+OT2=+(4xpwQq_>iZKmSNyS>Zq2M2151g5dx9|y45dcUI;OLbiYUi$PiGpBEjqvTSS(gme~kwZp6B%Kc(~2vPTE;4t;*A}c;44VB1X?EyesqWO&z~*E0b1uRp7WfoW$^kP9pT;+LHVB>hMUPa?qNn-nzC5#S~h*WEXt<*K<4ZYkB>to#>aE`;_K;qSxx1x=d^>Gh9X|#aT`iOf)Y;<2hzpO0q?`Ntk*ioAe-rJ0oh^{c58QD+uN63Jcewa3Ez7IZOY%CpVF3R4~jZQ2r{!@APETTx0|Q3_sC*09;;lkkcXBNsW9jJ;dFQYB+*FEA~DlVk68u=g8oyl>l@uAsca0@>CCt)j71uLK#X_<pZ7*k8(iOTF{98YL-tyDiw0jRiMIEX)${KoRUE?%g_943#_D1HhE<;$}vJ75f8A!);Ol3mN{U3!Eqa~+|^sZ<ktnf#$lGJ(&d}brJ^A`H3SK#q6^51W1}o2nWVPM$PmUK?;eV_W;E~_icR@dBkKd&R^C?0%4BITR@a^Fg;<UK0GB0mPIiXD(9cC*05$Z{rf&#?FD1`!7NeE{00?vvDyhL4n+!LA2nJ(o$57TQ)3p>=>nX#NF|aCOI;a;$tq~4VbL~Ky*|r58kDd+bDLFr8iGkY)k5$r08({ngLWNS4dJ&^h%uof&D9A^<rJ5x9MXM2-VW~+HVI||d0}w+>$NpL|ZQGIia}q)>*G@UQm;{S}_Y8P{Y=b7JB->l7e$@C-n2~T^0Z%rTQsl~Wz1No1W#s}8?K$hC6+jcY@$fA!UxnQDy({aZG`};xz^9SF`!2NL$FSQxWmusP(uvzd>W}acD56dXj0S6W&F=}eR$#E*R({NFvJrG%LPYej1vu+)x5zRoEq!Ex$ebt`m2(4<{gb?lA)6hycHN|?y$H(-Ap!N$Fj%+_StJ>e^buR4VgswGK9}Idh=U^JZP{29^2u`HC@<<W9)~$2NOCazs%RL{++{M~J<;Xs4FfbFKZ+`(V4xSIx)jnjhWKJOoj^EA>xw`M*)J)t27rK|no&3M-hr&A`}UWqTG>pR5^aQfp%gbTnfR~**Pj^8L(Vx-1kxKC*CI&sWOds{Q()k9yQmmd(Zo&>NyBytk)Aoj;gyEOI$tojo7S|)=9`yI3&3;0ke`uQ1_K%G>5LdO8Q^pOeb8ed$zBFO-fWaKI+nB{rWfgsYuO0bIG&F#g>13Vk#a?vGHgpu<cDB#iWy<{9|~jMUC^Ksln9VO_8{isY0dbOTYA#o)P#L3&CC8XiAWr&I1SIl!vDYpO)6QLK4yaJTvlFU5GGE4<fzEZt68{fE*3MufuzS=09Sxxe^5q>5(juox|aH;$5depBFe;!&JoTS?BtTLqqgnwB|UG$HMM5DuBuoII9L$g4`9aJS(7ku_U>ALCDBf;AbGW|cShl^C9esm@}daakV|y-4wHxtGKV|Yf3w97>nMVJ=3ttJnxyqaciB}411T6a`DZ*#+jn%OPsQBa*xU&2`tikDdVPR7w_+vs){xO{c&7&T@7lK}+Gqm=>h^bhPbOrd{v}|lK=&xV7w3tZI+H-c+N0xjIKL*TorksGBjZIgGMvR+&SCM7mPEE;ZptFndhu+YrC>eO^&7K7CcVm#rma8$e=s(Rz0+kbIgLXCb=BG-Emi2R$z*(6W&;DhL%=~D%U}I-#g4iu-DF?+aZeC<Fi>0oAzJHZl(uRqxbo^xq#`ycntE*B0o17mz>C}Ki$z22rUf1~3~6ILAlNx$)k21Nd$kN;K0ypZMV1BuD7(mQk`t-3ttTflgTXXi24Q+?J1otL#FywS?Uk@8@&b<%p}!ckaGA`KN5*wgd|b?5!jqpFCH~&Puu4%TPHxGI161>ELmN*S+FX$x<{sxUkr^gTO*4W!MDK?yCuMLm68gv`J*gmm(*9G-K*NbpFz$_VXK*z~hHYwODZ95I8ioZd$IaagqRnzER0N=c=k8Fy+3O~3I6d8>`EtqZg$~}82jh$y9u{iL_%Vm|5;~QZQuAROQy{~m>mx1!8&Q$uW;X(-p5!V@73F#Damfgi{kenMcGvFP++ig>$AMNyk1~CZrnCSKxeYRP*o#UAc*E#IIrpc%wXMW1qHh(0!o;_82y9e51Qjp=_R&LM;ha><I-wxUKGB?$I$lgm3R<;yU1)3|a&P-&_mtsOpQS<Z_QkX@V<6Mfzq(2}5r)|gP3}^61LS=ESj4{7268rxAFdnWqVHKT(jriEfC=^HBXh+Sf&#hs`r251dmgzNY=6a6MO-@xgaUA_+0Zerk|vz}T-Cd7jEj*-(!ClFkxXLzEbNAk)eak`OUUzSpEU7GQZ@KIcL+cchg?s0vwGx+@K5s*I_g=D-Z~(%nRSfQB0&X0ww1(N+}3*q4S#Yz<BUPF*aUA`M3FE~6un}Ye}6r^D3=Zq2YF6`49;>Bc9|j`Y0KKKgy)Cp<lT~})Xp`&47fq$<p>1vbSl^bLZYH^*Fw5r3Zb}*&tl^&vDO(tFL*!`)XN9~s~N_#QSp2aE+SaL(=-f&3Lo<I5s#O5P1?{9odNCRbKGR?lFp>FyEHEq?q<q<D+oe?TBMA-X@dr`m?%6<7U=f)_E2EZ=}>ia2zcyMlDQ=)yHoYM2D_PsX|<538k)F{D>}!w55?7m$fAJE2RKbx*}cus<vdZVOlK?*nv8ZK9CM1^AT4pVU^gv3_gf@kL2X<S)OIOt3I6a$$7#KlP>{9NV?vIb9yaDZ6>owq6M=X02mMmsRJopy4Vl)iU)?_#mLcVuwa_JrS^z!3HjB5$D4}I|pv!1%r3P^IbVerH`=N7d)2cyY5;?+Vmni}*K~mCC)eu~ysDdf->_LGtT>_|;8(pe(nTPXQf~k9V!KdsKEceH4U1m2LyZB7;pLTl_5<j*L><mbnN<pR2{RBWsM?)8zuE=8fp%zE^;?}@1Ew72nhNS6Z$x7npeu(5{GpHh6#1Y)JmW)>SPJVGXtuexZ%9MY{H0Iq&vj$_P8RMY<gK533W=KWmEqqWHBf04~G}w@5>zX!STO3C<o2#VTtpOjmr_)mIPI7S;bZ9`#mdNgTlT%99Q?9?}28`#KZfEB-I~1}`GVUurV?{M~s>g2EfTt34g(S=b0by5Ghm=R6%J>~ucMXZShck)+G*O1rP3?#u?f-(}m1TU;Kn#?hcwk5(GL7RUDQ6#9t5?@dd&}jtr>T{CF(3-H2k^alQrz4Ndkj8b58pS7A&oe}kUoTN(J1?c{YHKjhpPZpat0Y1(dbPBxk>>f1qBp@T1jKK3TE2}T+&4C(2k0RM9u(<pQx#qK~K~k)jW2Y=B-0Ja|qNS;&p}Pbv*Fqu|Nzu`7Jp#i|62CE*KWwLiBfnVqNCK>KmC=4ztx@sti$BzzKr@IRHH`8nsbP@NpXMnN%b=$6kR|7|KOkVjD;&4T;-Bud4jFo5A=7Y-`K<)6|Uap-oA!%j?>X<wni}P9QR(DVc&poe1(E3r+#6o1tF}-1D?C(AGhoH%ic)(GTpXQ{Hz-v1$Oz0-|}X#M}~Z%8fhh<rMn{R&d!74~F`smbJzQH_53F^Z^>pxCPt>96UOg+dVm<Yw9Q2bcKmG7Pf>fHrfYEC{_7Q>~Kd;D)pL(CuvPC9CQW&5T`d>+GQ40G{#IiTVue_KGbW2;N}Dy#(eDlBuJEIt?pfE5Z<Hc2<eF4fpNl`Mnn(b_YFpbp1nqrY#>BsKw`Xx#S<7Z%987{q#zzOHeghnk!**>>99N(P<OXm?vAXHy^eV>Bmu2D-=!ejCw$UlN!$jb4$2guHsU)A?*R3;gNhLAGUT{+Ad$rUJCGY-NX#Ru1&1p^0T=MPOp=+@H8^(%6CB7u35#hU=Hv~Q1I^|5ZrXxPJXnO?#?Vm;023~2Wq~+{E9k$vqA5?F96mOawWEjyr!)vcfoM2qXC2Bhcx#mkbfUcLPh?Yb&6p~KE)1ud({)vO+JjzHnqphTv&AL*h&&d-f~{qys)dgJMPiN>C!ui)2oyAm$bpxbvt4FrmvNy$rD_fpk8XhJG<R&Q^~n#VMne<r-`z)`A`_jJr(~aYR2O&%GWj#1iqT5SsSg2;I2j%BqD5YVw?)p;Gpd|o0jdi@FGyuiAvLSE+4;;ye`g+>$i3@{1?AW!aHSb48ml*s5*6H?Lx9d7Y^5hb(~a+bET_hZYA!`3MJeKy>WBiN#d0CDLG$n>oEa2H$Du@}B&9Vi?16+d<LwPY+uKw*V$Wg(f*L#T8VKR?bdAYRsw_%jWupF&ufaqn>J~as3SZ$RC~SZkcGB$c*zTFy)VCy*ByfOH__k`SpLzUW72Ex4)*<2jaBa+{Icc&FyzDXqdWRap5D=IWH)FV!60rIDSrK$1jkG#JL$o1jB##<A$sv_qVKX+GqV+(K+eqk9W+)@T<VN-e1uY3m!I@Jo1#*it_e<w8S7N?-MSdQ^`I7m1#J&Y^E^JserbY#CNDO==ZMNi^E&+OhP94wz7v@R8%JGJMZj%MQrW&kEodeO}D>^GJh>mDmE4O7%@LWHPGl@|!J49k5tRwP2P$6$4d&VaQZMn#dm~@N63fH{#q)!tv$s&R&V9V(J;~5UEK=mN|oTs3r0c4_)LRcROTgZY=iVNaiY!JNF;g_*qMd?al!N}}YZ>iy-0GBGoIm<wm@D_<}iPZ{Bf4ZW|GEiW9WEV~W|NFY<p|%H}4!UIVlItp}kA!7nHWxeMN!hJR^tuo{K;m0J3Eys283^W}OqBk$z_#RryrZyS`TlaVn$D5JN@sxy1|G%sX*eFyEG4NFfn14G$wmj<l}Oa<_;yI-mYtLe76SO|+?90X5ye#scfO=KFozXlQj>rmU(h80urCojLTKN*1Hs$zw(6z01iKYZ-T7t6;aFb^S9^S-0|85?N<wuuJbK~v7PS~cN-DHe0yzdPFnjEak0m4e^(NVEY!Sl+ScU}RJYb3og7C#i0^4%}qdFONY#zcxp=>@OOteWAK(9h0b|SyMZNa>=hLJ`DXyWPR1iDbx6om#>D^Li`7R@tSFT2P#LbU@K{YVg?l~G7cQZenYBQ{ueq_Q1#h@`57Gn0e>IMev`JFGIO7REoXuUrw0L=nXcE}tP~9FgZD+5AUWR78W1;fYaoi=zH7tnTYj7k7gwM4+~?-<|~|RhTI4d!Z~pX#DzGILCaUL5FJ%7hlyF&g&p}G@BV_)160==9OhDRL6SMtK17Zx)jNS&bX`TR5t*%N_x<zj*e?z+v$s{jDRCYCNZd})wE|kXim8W94D&e&@n%+s*s~fSy6qXOR+7-I+Tn<qMocU^44hNa&|$pN;^D`I%4r_oy)5MRA<I&kHv*@@Y?<tg9?Yw-34l>YRSG_rMb7I$_&JM)|(}hblv2my?hzD5s;bboQQl_&iS3MwKTccTFX3Uw@4n&)P`L9kGS-vWGdji2h?L8_fY^D0GN#C&T@<fd+CYxF~oS-0i}}B^sqVo%}7><=Q*v<H?t^K>8D`k(f0()&ly)jwSbj?^%CkKA?RhkAW3D{A6wPjoGt56Gs$0jUI$PaEx;6b*n+Q@`yN?n%c2mR6#=!Zu@=2sL%2}A3yUu}uFCCd5y3!2<hDS7He@<-9a^L3Gx^-0dpeacbt^CkBv#0cONwGRi*1X@l3t=_aFu|X0kwOc8vhLQE2UxCW}m-)*3(r0nZ|u8Vmnv?j`n&<Nvtdcr6>f`8ju19SHv6}U4Rz;x5PLLj=k9RiArB9pAeapq(j=-%mfta@7Qu!lt5`jCq0D7SH!u4m@CXh^J^XkY<i==|8QwxnFS_XjG-un{qZHQ7wNT?dX7#k2W+$`JdG48=Sn`7ZA5jYc15eA&ot8c14`6V%9gx3&2J-`A-(1WgH<*lzqBCo*y3@RuR&{npFU6<L$m7DYwTT!f<uBKTIPvKYjfq`b($E(1EaLa5L*ny;%mAZN#4`dBJJX}#RQmKnHN*FizFreG$!Za4U2|jB0MMHIE)MM9cV;O!FB|q=?gopy3Q17(ycYJJChBuA+X#X+;;*+wL$VSYs9EJf-J<d!;1!nB6`D~Zn7ZL8A(#qm4*$l5Al$Y_eF*(Vi)V~fWu3){0`J}s3#b7HMoIj)4yAjJGJakUfE<OQNnIM)w4`N1GL{b7}k0-Ita+E@(AqwIR^dB7~fq#RHJ0^G~F8@f!5)#a1QYP_3kN#2n#rl1{e~ot`{o_xwdzVWL$FqbC{g~0@k}D3=$C};u#FAvU%)AZK@_+l@ZXkyKx$P36M<)8!&*B_%d9HYfj-LrD9)&u;|KP0UV49h?w<Q7JgBVv{*I<An_-81jJnZ6|WXzkGZA*01VUbqx<_z^H1{RjmiKVdw~IusZ-pAC3oe*aRw$tJNJCFvl-m#Occa@>FjaGIBMBZv5tui|4dDbk5^nvmO^E|TA#F|zFDa$kI=&QiO@Q8+G+_b&Xr$y@aW5{7^?l5{8Adjut?WyFmPXF!M>^*9;nnU%4|2GxEoZF%5YKfuIp72ty@s3c}6#oz!c(GD26)OghH&go{1#55%!LUT|6T@Min!LhYKMWk*#CtC()u@&~x{>uTes>r%nNNeIfT50$~{_P$Bi2cqznb_XCWUaqs&0-b^utR<|1;I;ox)o!2}g?aB?(W?-IZ0o7LZ*0XcY`jHS+Ki7b|t-&_+gK6T0a+c*rgU8odn_OLQ{pxz4Ul(V$+S_uGKkSa!=P(-p)~n@1&CjG|SHwKA1ea=&@o+$|XM1D;Q~AsP18P3h%K')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
