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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-qxnO^;hia{Mnk_d(76kmOsh#GMgVGd++rORN{dU;wXSz*ryFz8U`S?wRJt<IBj1$gHA-J&7P&WWB1as?5m9$iM#Yi+}(1AAkSbKVJOHUtj$6@afZwFIO-A<JbTCxBq^6<LTw!fBnaQ{_TIBUjOyQ_wPS$pFZ_o{Nd-n{POVQ`yU=YytsPt_Hp;(>N>pr>HF>Wr^N?9eSCcP^V`o)pX|QhK0N*V>dTk^yIKzL)8o&dzh92<^w!hp-@pCS&p)lc_s7SN>yJ;PiT`8y#H-&veAD8$PhZYo?Y5sjzxZ-Ko1eBHKAfKPdi|uwq3!=*bN0i}UkHBV_nCbE;oUD!OZoZd{aVDIU;Ws-kB>iPPxjM?hqv2wQcttL`q|n<zJ1sa_4pz_MSN%fMdYV|y`Ztbd;i_}9PU5jE0$P!wvY$2TZ|<>5-`$*f$x{%^qFH=`(b|CZr?q<{loUd<Bw>VtM6WnGMgQ;TqRTAf63w(p9b^e=i^|1`~L02{<n|6czg#~fxTAhL{gI$Pn_i@efYfnn4e6AH_xY|vfSC6@7GeCW$egY7~%7Co)62Iy*P%r?sQbkXNFdQ29e!0n`}pjwLR_%a3;@KxU1$|9)}YrH6A;E{O#LE))JiQ@pl&+BAjHWGX<S#-T`*@b8xZ1bqTHM@MX{MHB5W|i*SEMi#fdz(_gd-uqwx6bM=VKl4lLa+3;sJvKrvgO5NqD-+^bps7&bi-tkhJyneupz$JWo6;4YvkWJr^i2cNmGOHu5+d39GGmYoZ*jwbA-#&i$uzmaamp^Vlet!Sq{lA`1aXseot`p{ClUH#C6CXy804yRoikMrqn7PUT_{1llr*E@EQ-=ZU5Uz(ywUK8JB%gx^g{O01?HgZaIpcAD{N3Y=g`Xs!ZhyQlBai2aUcAs(Q?fmJ2QUat;u0ip(np7Le={=oxqrOTU_@c!<f0vK>9td-9AYDwj_VPT1MN(SA0fUpy8HoFpby^D+@xQf-rb)*e|*^eVf*ppUq)Q7IB|!?S$x0ueAL@TQ`S1M%hzRPl*BE5{)l|>{{NzLFg&s~QtP5#owc>ELoQ=wdDsY%WBTl!)fOj>j-2oNC-(7*zi9%+;GDUrbAUkJA@|O4%;IIVh83;|c0S=YI{GOs&oB9d+A#@l|Kni+H+~KxpD(_DPclbPpMP-~k6%nYLL=}C>vg<_fg3^0j(cyyYFPTi16;p<`1oi4sjb^2#Vos5s|LBO!2=tM$ZK@{jx%IBQ59Dq%|kKts`Q94`L@pZv@k>cka^r#+`%UcU3~k}Y>|iLK2XR1CD0yvLa@W2r{%<!Eq5JkD1bmlXLWJkeLW}{&7kj|68BlYD19w*#=(FM7$!iINAyv?XrenTb#!BKG77hXOJRUt953(u>ja>qgMaK!oqk68mdc}yhjZ9r&>1QEaRmBG6IC}YFU4?T!9{)ala>dgdPej21t=UXB~k$7VL$=kcmo|Dw{glOCI<qM<8wT(bqR0=_vdlY^|)>`fy;6lQSO%cai$M7kGd-HtB+d`99P2iF1VO^@WgKV6*f07bUXdj@)1pR$bam$^PG9T=wW-XA0am75y?b2tb;oYc#c)Khr-S+1Qp?bkWV-Gq?C^dj)#JS=Q+FJE$QR2ZzeCwzT-_F?HqIzXJDGq9g?12KBkgK3C@0a2G;#X?7lHyN_w*ObDw1ELPD$dz$7yl!8`x4+RkDMD<pCJ7}^c|%b4NIayT{jGQ%f9KvME3p^H<GpSXYNxCrbh0~|2u5jDnGNttrIe)OaOhuZNX0M6Nk^TZS@N%?!t2eu%>QXDP4${4qF?hQ0crx1QD_lq5JnCFS}H@G)_LQ3=vvmF`_E=Jz-4-Vw10C;cBQiS#}>>OIxPU``VlT~nN<2}MClzq4J_A4aWXCRk=dq3==QkawbcmLd=C;h$2pyw^v%Tp<;4jLM-<?2A5j-Gcf#*xsYGep-So~H2UJ&ZJ_s+aLh_0E9<8NpP2<hF*Xt}thFO4(IGVA5)QQvYpIy%a--+K+%BFC{w;J|gltc#<U2Jlc@7cMWy&T$D`_O>;H7H8Mq>TwygWrD`VtHL}aORj4=(&!iyySXzMshm{!_nC;BHhTAKqxz~iwF55HgoykH24jZLf<%$Yli=HLKSHZQLTz4lX0dk6}P-tVQ@yY}Sp^|1*S3NgR5_>GJp;MqEeDQcQBdVDT!|om*pZ>Y0_ZN#HNR96C(Q<NS3;!x$bkR*_oHYvx9+_<T9CaGzDejGXomCEpQg~=h#H(8v3$F^NixSOAL0+s1C18B3FQL1r2jDPRE$)YuUZ4nGnTLBcnC~7RKW&SX503HW46b)Xi5`xQN{}NwnB#Hyb8-2+dOOY2(~88%mCekwqVUn=Uf5&dXKn;Xvi&e*Y;mW9Va02Ljy;;sao4?lj2mYD4WeeA7dEJLko@-j9`!fR_26;cu)@=7f!qQ;^VsDx<*K0^V5qSH2qO;7_gk1=yeGj{O1@;dg<1>ISs$87h^+Apf=Y_-)?1}_M0e^EAW0#Yoj`x?NKwpFRU%RtR=km(-CEhBQc^&Mxk6NV9+*|lqEX(INL>t<jU!-X60JHNVwcAt^E95AUqi17vL&-YldrAUQ74NPhYMVAQZDFfWX!7tX1ZkqC8Jdi&S*(-HPP6sHO&V5MxVLI!(pLQh(`*%sNuqm6|0}QK{u1<rjpGh={qdlF$TtT6ipOPcS?Fj>5q|0@e{>N2&s(C&1PgBqaJ3=2d#ac8uKKYFRPK3zhLC*Hc1srO1*Aif$M0yW0xdzn|g4~EL5@uz$7v5r{%k{d}cHOMB)m|*{C~etWTW2=(6Tj0M23Iv2f8VpK@bL=uoJ0+u)a3glQ(u*{fWp5AwWzUCyirh&-=g)7?kr)DWqO304+kfuLbD(V88ZrC6dGW*8paGGQp3CMWGV+qH-JWRTJlL&v<{O3BB>NC}RWUB(nlMt9KO*nW8b;ZOTqS9kcJ#%-IrL(yHNImZD}B$(rkVc-e7NCG~q!o!ckh_AF*3p>qzgD*lEYnf-i{2traUOilg(rdw?GC)VDz3mtf&7$}sZcaqp1<)zkuiY9M9WB6lmFqvv^)F+&07JGzREYf%^%hrZrU5{M_z-j|0N{T1Ut&682r4KGjskk8>G&5*9w%$|$E}Uj*?<YLZ5}JKw6gxZEy9$)xn&vB!O+&slWQ}<y12QZBX>(q;YPU3GS2oIj@#zaZ(U_K$wzECU1RNK<y0CY8Wnse<UGB<sve#ujc3jgglay}I-$%34N)C9p?td$5jU{==sic$$BSB4MxpFwvdMJ}T<PU@!jg2%l5+BnF?MPhV5sp1T9`E91`}FA!|rcdx__)EiZ#<~0T59A(gc86nI=s!LqOr7+L=vWNw*h=i>_aG>HJG}e6D+&9ML0y(Y3RiKzS4$Bsk%+IspXbc!hzTw07PGCq=u!?EugjDPqAZ0H`#P4Brv#iVTZXU#;lfw+rvh%L86-Dx5)(vt>>-GPYC9ZdnWWIX*xB@bLMuNFD??i(INm^x6OP`Sm)l0=tF%P$$W$0d1&nr^+y;B6T{2H5qSatO7Upa1)}bI20GMc!;HeE%uy!j`tsDB;Bp7odo?6kRe8zh6P=Gf{{E#!f^ZPv-JAXdhxQe&5jr{b2v~yn{1nAJ*Py_acInw&f56lqId#LvH)Sz#;|w-`Ai)P4AKHak<VFP6n2fmic1!^pzGG-7z`V@1HYK5u(TU?GYD38Zx)<MCm08rEE;YSdRV^G6PRa8Wc>rMT8ZzT<IIwpXCa+d8o>cLm?qJ?2ZP1r;?~zc4u*uM7_>2>tY619UVj5zgV#P7?3OVoqdHtlSyS8=iUd0ULEil{I6VxV@HRMDwys<j$Lh7Lg5arg$*oq$z6yLzy>JGH5p#HEfLvE(EX4Jup9l<<H&<VcwOyofn>^9cba@&CHA-VZ1-zUN&+?pYx^L@KNxd&tJBodEN7c5Zj^n7;(L6EZzN96w+2Fb;2HfnbS|&aMASvMB)Y}V={nXX+*uj=;6ymY1P#^Xn*PEEQzvaqic~O%B=|I#WQOdZW_9c}rTCa>eVrh)igEmaG(ptMbQZuDx2tC{vkb5dx7q^pm4}jfEQ&FZ&ht8D9zRWca%PG-NFg@t+k!oUE>tjWpkO0MX2nSUFtR6GqEvUjxQ%HVtWt8aQ8EuX!rDD`hx^V95#P|sb%(H|TLy1@PE07wygvoiTm}X70&zS<eE5BjUh!ui?78H)q)78XMpTmZ`zO=@oU}C=(S$@t69<?3=d5n!#pwtbNW5y{JTQEPITVJ*G1rLus3v1Gw5#G%GH*YlhB+E}WV^0L`f%t-J#*({QQE2K}aqtMF3-#JRFj?z^a_=N<E7MujPf$@zXRIaJ3{*MI>Rn^Fw+?mFYbE8suw+Lx1xw_(EYnE3QPD{DbxLA#{A*z7Vwrd`GU?pe0xYB5GnR*G>4*OZdy==sfa4jbohneXpBPPeR!1x=fm<o}F&=cw;De%jnuRsmAsv;;y7_&dR>;oo9EvJG3~LNY36eV(!Ux8GiMS~~2<kLI>*sUc$>Jbcy2GVS>``QS*v%k?G=%l|SraTr!h|%HX9?f&%?lc!w;sggH@FEa){taoHh&Q;F0GV24GK@sR2CvUkn_4{oITq%4}ozyj4Th_!E1}UuOg3yGm6S13-crVI<%VI9nU?~rO9QcXjaQuik)4ngDz;1TUNHy)ii8dDwqU$(!WXNEdW@bEgZ}6Zom8PH$=dwcZ+>OAkVCb%&c0~O+{#4T?&qY_Q<4eR+US<gK*w|Tjr9=4N8tNFz~mIZy9GXbvI4=`*YOsYMEi(m)n#DId9WIM8&IAx5@AP#5o-bgRx_ioqI(l8&Xy@k~Y&c9cqjx&tt$PBlTF<ZPG*(8QO8G5En=9>t`Guq)Uw;;*qqMSsJ^}2(hE709aIN3_+K09ijHxln~Z})OOMa&i(T|_EWXJjMorzj8(wgcfkj`yGP4F13vd>YO3W)aL{!&!9hXYNaQ@u-ESo|Q@-_C_4MLFde=k&%siho5Q3+8Lj}bow?IZS^u!!V@j$`#Zc4R#p;)%JY<@4X0l05OdB@i1CB&+Uz;Wwva;IXJ1^X4L4-+3`QNSD16^bsjkCK@s=(NXX7cg@G-vr?BL2r`i{(aBB*8PHdrCbt%VY{QXhcB>07#-Ybr|WD4Vg(!&Tn>DbBtUO0U23&HHDZcT8(t@G??Q}xT@m|K{G*Gi!%Skf+|=kUPA5BBi1aG2uqs#g5_${u#b|9x)kDv{p!fnfy|CWI%i|8j4c#6qj7x@r`sTFStQOBT@2hl5*sWouv8jm5Wg0FkcFZ*rHOyl3O6)BR)PPDY`iV}c)`)4o<`ls9yt%V5>Pn9R0w1{<#<-<RdzbWPQSdSLz({IOBLPo?`1l9}F-r6_bwo2-!(qhxfn*P~__#scp5$p78xiI=3M36$-ye?Glf#($k&LX!0v|-4JEwp{3`YkwHH!k&#{nW6QEr^TTF4K73&iC*jV_{hHMYGIn=;$4i--$mWuQ)ygAW3`kww>D=H9IhoCi4gVlbo?d*$q4!bWLsvRkO%oH^EG2iL}Mx)VlUx0cY@SwMT+lZo=gXxL3xL{AYzwWOiKK3mPU5?KLAE{%;dJ<Qja0u4BNX+Z^&a#1OSJhQkP0M5uK;(UR~(ty5;_Bnae$YMj58>5Q={24b1?2AXFM=gcAhD-HLVV0D5;n1E)jvD(ZO7lUBk{85dA+GB8yad%AqbZ>lSu{x%l8DeQfZ;%%)n>Ap4{i*R(p#j7jo7m0l@%$S=UOE^06LE{uj(0Ojv>+!3!NfE=ECJ#R2q9(1!^S2+^p83ogU!aDzuR=yvTZa0hf)W_+W{?O=j4!h{_7cb$v@pV#KS6N4z%IiPov{Q<wwV0=|=5mBS~zP7CEw>9D(5cS&xB;@E<zWzdes)6ypd#b@EGg9gOz1>|C0G!1rLt;fmYpi$4<EpS4*hVFS_*DKaxwu(Y6saK^Nu#8%kD{W~5LZ(2c8SRa3k)%E(zMzDms&2=c3$YBh_l&x5aol}r)sp1V`{k-g1{FMxZ!VYbPGKE{aq>I|O4wxZa9}bYjjk@sXTP7{UT0}+*Ds^By-DD(`$|V)CL4l|MNar88@>cYsc_9#h?4Q1{07pm$8QG=HD@4on<{_;8H7sAX+S1KS43T?S$W~AFy59@ZOP!Mh|^SlQ1_pciS1($h4M_a3k#Aa!~mEGt5bQ9Jp@-q@a&d=P%))lZrq{^Kk|e6zEJzq5k)XrdUZVwO@vZ|Opq`&@7bSP!qJqsp%ANV!!h9B1XnA9(axh#KDVySHh^FO7Sh(5n=jowygn}E$--GRO3<J#`HC8{D(i8jaRl?JNp8v*AN1KRMFCo!L|Y1FlE8)xM2T@<LtcU1YF2@9TMsml?}a=$`&<j(D`rO}X<)XCrj%q!kh3^zO))hF2`L>cG0!Ebw5ELzRh-F*Hx-Sl(pu80SaDp0g|hUs$6qOz%rr?Z%Lx9>*CVuu9-5ra!rN=P$MwBMWGTWx9AAj(^#TRMZpS(PHubs;UJPbi(1f9pnG-g%J^@OULnVh{mnAP;D5@Z0wFNprz%sUj=R3^k;JZ~mUMh=H3i6}<Gl~<hx@GuKY3ZS{s(mR`&%l+PYW|nN97%Ej@B{7ELpvSMi{cB?13c7)t2MOsF_H-Qhv*N5;*SI`y806YFJ)b)&5WL-ZP`$5k+TsSQx$-lZdzBtHOE1fG;v%S11UK*JeYd5@l9sQ9jw~wZYm$+^*Y5FTR0}vBtD@IUgLm=z&EIoVBl%O4aB12BnDR&)f_C;0amBGYlyK!-q^x@pwPz*&V)_8^BujMk2QzH1Un94lNNj@Y=?zgmYIYn(bTP(np)bkD>T;Jsw$pZVb7+oxS~?M6c<VUPhD~4P(8C`5abND*guD-e<8}kiiJ|7ra%^uA|t0t)34l-IXZ}am62R}WM&yrrI}9jEggvwd~}t<`+9T9b6!$a`^=CiDHIJ&lvAm8{APkA3jOzmAneir0yoI{bUiV9Y85$>F*tG=R4W~6-m3+gft{~ca0MfR@iA9)Je#FPw2QMRx(3C>om8WS0wRLr^%cW5KGRK&*1;O;Q2CP`L0Q1^D0<p{#IMSV#0oNvcHvn{udLbyvWxedmtV7l!y839j4Ptu?-3;cK2#WVB{69hp|S%RJ|ur~ny7ix;#SzNYPU^U4rok@K}N9ll_Js$xJ^bMInm4{4(zjg28y1%d;eWW+Q+XF@>*S0$&WotVQ^G7^URmE8c<K|fQAj*teyktniha54?nROaD%Yr&^33=c1k7D_ZK2=ZELdHG-=4Yd9Lu4*BW0jE0m6Jxw#91uE2U%ryR>HXW9c!o3uXVTNXOqWJh<K>N2d+lEN)+R}ScRyL=XOR}bMz`vCPSHr*?<e#hPdr>>aTi;nHQp7dJd(4Tt5BlNofxf988azoa~<f#nC9W+=Li~s>;i4-FA7LDo?C6!}W{`jhDQUt}82ri_a-BUwo|I`!e^nM4IbDmB<{s|v<=8g@=sadhW`uf>O<jw4}<j?voI<rl><vOzAFam1)D<G0cNntuIQ+li;r*E4}1mgqg_+M$m)E;9_SdZ@m#E?nESawa;%M#8Mi}wV-&xZk1Hde`pxvgPQvciv2@!|_=LpJX!14Yi?-;-XOTRraULL4dK&<f8m+8el-&1lw9SQS*_QdmpNXY&4?^a9MS>UqV_K6*aAcq{E%?H}#&Kw0*5Wm*z~cP_eM6am5$i<V&t7SQqHXbSa7*=D;bsLD_A%q%(DE<?NVxH1ayp<av8gW&oa@NI6a>x0Vg5{?Z8kT@7BikN%?&Sm*F*R=`^U%KW#{qsSt%{Zkf=5C`*uMlk!+BJ7ZQBR$L6V&w%js^%b?h~l6%-rEZzyL)sxa4>y0Z=o}<ze!)G5tX$*N~G#1Mx0LO0gU(%^7G7OkI9QDrWK?<e5H%V51Iq$SS}vROE!#BzHJ3M0Q2amDwYSE6p^VAl-Qx@^)xxOH%(fw^^)RRu&J2it~?_Yv5S$HErY{SQHJfSgz)Eky;dfCxE!$JA0eqA-qB0c-69awQ7|@{)+W;R;!kXp&q?@bSbd1^k?3*BSyhhfNy4pDw0-gQ5cP8QA+OSciM`ts3jDNW^hZqo+_Mq!f;S80X#{NhS(8j9jOc+jc+|(+bbC1b{`Bl)KU|QEhd_t1uVa2TaDK!35OQjeMPZrl!s-Ch*7ADr;UkDo!lgE!Y0}D$v-A}-D7D{T_JtUM$QkqJ#$%OS5ayW`dkR%xu{-^4~wA6#)AB=|0ZRFxi`Qqz5&KGZgjEP#_s-Hs;T$f%5KbC*QxQ-ft&&{qr?f%n2XdI5@R*WN8SV&r&yVQLTygno+wq^soYMOO8y&qm^BEGtJv%~V+rsKL|VJu5*Fdwq&<$^01Nr2(8-Z!W;?SOO&l~ezzcwE#Yy(OY`eYn-p}xm_nJkN^cuu9_Io^hhp_y5;ero#v1X@EoeW#WyBTEjLia1b<$y)jY!XCupFUIDvMAkZVRHPAJYWx^WsX4YIxV7JnWpkQLX^8ZjGcuWn!Mx&!_68mQmD2*g|7WpLB48mv0gA>E~9OFJQ<nnqB|^c!k_R+nWH_aVhxj`W{FxVrv~2=bv@r?S+&T(I#PC5#4V{=(q2|`WP?z_l1Hn7wC7UE`^=N!L>}8uap6=Z{#VOk8K@ug((LFQ4qP2P0gwr<z04Khde8b&(Q2-UOBMQ?V&sX-E0_9hZH5u5%yA8;%Oz^jE-nO=k(1o!mx!izXk~wu->74V)wqBV(5RfEzAP!bx9WZhnC0f1$PQI{FV7<`F{L(Ew{5nwX{gCE=@o^pR4U<gcdHpKbW2)9;$}6H#x>#<(U(?%Jy;wwoR`VU35v6ROKa+C@}7Advu<iT5;&Ao4x9w>g?d5*(u{)hH6w&2@)ddYx+wQ4k6z&j+Z|dwv1;O?i}I>+jUfRl8e}*W%2m|ibWU9XMi%y~EPf&pLfC`LMhofr3L2Us3=)>dtHI(cuMbwcD-qnr5fBi)-k8IZW}&7+a0C_PcaCmqRh2_uFg7j#V$q^e{?IDpqXeo*rP4U(DHVtoy}0rhRJYr^H>i7W5tJ4`Zi+?=y3mYrH+bgrEpBfK6>I-4{c?99f)hbq&Gz#0;>;bTLs8G`3c5sV*XplO|E`&8(#vqaPULArNP=A87rH6sqqdk!lsDR3g4J}&nMLgms>{P{y<RzdFm)gc5PNai1sxpM^QljRozT<sHocQo@XUHv9p5=PUG&<bp^_%R#0;2?N`&?qaD3pD9jrC5Q6T6QunrG2k9AglexAG>Y%iwtFQUQYRH|LR(vj?q07QHcCOTsyYTZ~s^h^`XxDy*HmTY+P7qfHkvf~p-ASx{_o+%ZMH787P3P>Kj80rxP{ND5Td`*TXHAMQ`LJ^+^2GK%S?@X=S;02UASfpVOnf&rTN==Mbb~FktBRMIqNSX{@%?80&H+^E2aE{GB>x{eNHV~a0uqx7~cf;rm7DE>Loytn0@-pJKN^y#3#ms)%mHp@@ff)PKI%p7PTDiw&tnrq6b3!}Y(+p_dTS!t%@>}B62I^^aWx3#4t-ZN-f1+_l<~y)3E;Vk}Gikes<qbN4SKlp$F87T_t0+cw%3U1(N?)?^`^udp-Y~A$`H422Jay6XzBk{PKDF~Yo_BAOz5@6#UrM1)0o&X)Th(ZY_%79h{}w!{TxeT{V;7}HZR@(2f(kR-tj#A*IX!=U$J063#+$U^bP#j185q^W$v_PrsD1LPD|ipzp3}seo91RB`<gPlpVC7viLzL)Glx5sC`Hv<hmTUFL<t#uJnZB;TDUz1CU^3?v`Uf(uUEq!AKu6ENl5B9^fTtwCPP_0rcELXl@wOWRU>s6j15I&0^XXy4)K_JRaOjmePcDXzz2muM2ix&T`-CQh=mRz9*=Z&p4P0N^t(&wV&z_cRI|Jl1eA(hiyi&y5GU&*5{&!4*aG6X2m<u0YVWAbWi-R7Ndl2{_oh4gmk`QBs_UbhxY~g@D{AE&A&Vt=H<$Lr!Le$~Nd_MYwPFKRS{MxJ@kUAs*?%LQ-u6Xx_fut`F2;PaTNg<Vl+LD-G+*hYH^7~CvjHUd!9>6%7l;w5>cl9z2S{AN#kwWLV8C3L(}Qw^g}Ix`3vxPYM3$-+RrfQ!<2fWV2i~#4DwTezrrJcQL~9=tK+4qRgr}8MR~pty2UwKJ2shbJ(va;okE$J)Nk;i<6eolzF+9Jfy20xU@*wv$2y#crC`lt{06CdNOJfs%wT3yRB4V(YrONX~w2?VgjFVq>TdBTY5xCJAdRar}D+z(K%+JH7o8zUsIcP_(qVPOHAnV=mfFQC$xxllS0kKuBwDXE|INxl>zPBp^New0~I=ZBo709qy7b(;i(u+!I7k7hHBhj}(LKAQ`Q28m+HY=54L*~X<wP!_?!h?N4pkmf<_e_ytddznbW%I1u0Y>tpjTg&BkW3`1a_5smB&zg;)*{y%_wz-RBjs=r%J9?SXn6JQbenD_5RZIDg)S?-{#LR~5@jkh7KePKjY%xZr2{WOEHZItvu$8iq(CL50pL@)H*~KyxuZWkyxlI5ezUussdR`;DoX;jw3s&Yncocd>E`Vy$)|hi`MtgJ?LjrZ)Xg%t)7y}G6NMVU=I)@g3^6u9g`8q%VR8)_k4-yK!<4*>#W=P~wJoLDs<yRAIJDU{+w)ewzrMk92BH8<Sj~W!=<W*5Hv2*NJT4ha5g1<AaBrp)q8Me;t^YLh<5D0E6!2Z&W0{kc1HWlMKa1;Csho-0q>P6dQLxdRli&CbVRD!d2EEU!Z(@s3)kOK#B{dASxYCVgCW@XgI?SCf8Dun_^ODmJ8a;!?<jZ;O0%ln#DIM=d3CIq-A1eUj4+D3ttI}C^^g5DQxoEz50E`g7*zYyKJiE<H>;Ac^U}Sg$N8}8fB$XhQVM7}tdz~!x&DUdXmE@`}OVzp^s>6$q7B#6r5NE^-l&n5R#k%iDaXyl%=vqb`TY{n{61G?c6Tj`FJO-28?qLFquvHAAW39TKcAOK8?Fez&cbIGvS|LDgOZWhFv!o`>z$;iFHzB>98h(+8qcTL>xu_WOe;mA2?8>^h^JXTgi{U2)H&?Y&y597KbO8Rta;!VrhNw^=S!}LZt4}vbHdS%CR$sCaT@_dGOVAqxp9N2jB0A6w0~Af9<PSX+a|E7OgVOdlCrOQIt>9VhjM8nQHJC<_T4)K!r&HX^Oiu9lnaUfIF>z#RKt`TcWAz0IV1&%!xvM(8q<<QvE!9o6E~S|6s<4CanZeUhKxwf@CBLS1x%t}p@)2F3lI15pbe7^~5KCp1CtjZfzgIEqd1gN1fjDvtfT33&60V!uIXPKYP)dsVaK5sQ6y5*Rkg4K?O;9o4bo$+mFsS^#&%^58E#T<3P|6fvRJurWNrw)o!_<~`+w##lQB}QRF{aGDR#);G|5T|SW%VuT1mQ8uMyYL9iceOd90!0077%`7!~i2oQpPEu>i)k*0|3K<cMdllGo^JumaZ7hm~Go#+Hl97ii`eQlazeUUZZg#inl19FvF~%zh$Hm+L?x3MVx#}IU9xa>8{`{RO!*#IP#T>(XQs)VsAi@5omkH$UZ`hiJ>YYaFBYfAc${6E(03S7DU{5BXt^>)Z~~bV5e)aNz&gh%WPwh{HQ~puG*4Bb>*FtnT{dpDQjP2knNPagk381$~Fp3reGr5UWxHBuI4}jGpgDylO@Jz%7Bha+P#{qZE+l?&cmUx3{@ebWFztf2T<i2(QWSB2V*pxg%c9tmz<T8DkXJ$g^DWaE3~MWfLHd`S0UU4`6d=7yF8oc$Gl}Qifj^B?F<y?H-!#5u(TQN4lPeO7-=@^vCJ~9dd(T*IUv45uIdV%z6xK%)NNJ5u(X4Oo!qdMA8VI)KdLFqNDUhTz$E;_u9moFm0L?wOpWfZRe5i5WOW32h4PckpgA_m;?v#MWq-SB8Du9t2X&yk=H_LyJfFMr$`UFa#a-o4p_-c%vWRb}V-g|+#v5A%aD4wwL{D-84<O|&afa{~ZiD{YpPA{RQwGhMU>?eV(4C6b@$Lz|2I};-2NQ@I`mCp~wxDiA9*?ME0oyqxzNF6#{YMaH#o1vsD?F$|O^0tms8NBF7GWR~ya7){)yvjqVb|Y=Rz@dW!4!5ddyqkXt|>F+m8KmPT5E#ev<bu3?FHS0o(|;@RT;lh5vdEYnE~eSCW9y)8&{jzZB4kfTp>>^ze093ly<*f-+3p{vsy72N3m0<Gc;n;G+lX{8iTpgqLYm{Kb%V;R52PA@yJdW1vGm-m;_Zt{dY9#X|U8yP8u0vQ$5!KOLqBHQ(9!LvBM0vs%<2p4g;Cik#eV#k&J$8)5CZJlS~qAlR^ce3XNT4_|U8IHhOzqT~w8?0*Mb>B}Qfrxk9@?e{7KT7}-+&1VFb!@+73*+vh%mnMtou?~_mF!B<2=zSk@+p(2Y6N3#JFuu8QY0Cl4eO+c=UM05!!#P&lu+YG^G4}qjHj(u75kYnNq#Oro@z4Y5u_ZuF1kp|GJp+}rd`>EE4l8iv!d?_86ag6X&xL4#+q#Ie?B81@$6^o$zJ!W4SZ4=}vqw&PQ)=0{mOkBx%hS;FU&!;j`+nAQGcg8gK3F+DmxB`qmz_dKrfTIl7;c|HeYfG*e#dEz>U;ZEAM5*W')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
