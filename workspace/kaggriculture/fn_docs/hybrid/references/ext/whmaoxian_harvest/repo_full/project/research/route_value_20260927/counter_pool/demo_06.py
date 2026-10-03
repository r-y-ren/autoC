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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['NORTH'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['DROP'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['CARE'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 2], ['CARE'], ['EAST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['DROP']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FEED'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['FEED'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['NORTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PASS'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['FEED'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['PASS'], ['PASS'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['PASS'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['DROP'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['FEED'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PASS'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLACE', 'COW', 1], ['WATER'], ['PASS'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['SOUTH'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PASS'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PASS'], ['EAST'], ['HARVEST'], ['DROP'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WEST'], ['DROP'], ['EAST'], ['PASS'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['PASS'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['CARE'], ['FEED'], ['NORTH'], ['PASS'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['FEED'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['HARVEST'], ['FEED'], ['CARE'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['SOUTH'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['FEED'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['FEED'], ['CARE'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['FEED'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['CARE'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['WEST'], ['DROP']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WEST'], ['CARE'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WATER'], ['EAST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['FEED'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['NORTH'], ['CARE'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [[]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'GOOSE', 1], ['NORTH'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['BUILD_COOP'], ['SOUTH'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['PLACE', 'GOOSE', 1], ['SOUTH'], ['FEED'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['DROP'], ['CARE'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'MELON'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['BUILD_COOP'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['WATER'], ['EAST'], ['EAST'], ['WATER'], ['PLACE', 'GOOSE', 1], ['SOUTH'], ['WATER'], ['PASS'], ['PICKUP', 'WHEAT', 3]], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['EAST'], ['NORTH'], ['DROP'], ['EAST'], ['PASS'], ['FEED']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['DROP'], ['PLANT', 'WHEAT'], ['BUILD_COOP'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['PASS'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PLACE', 'GOOSE', 1], ['PICKUP', 'GOOSE', 1], ['WATER'], ['PLACE', 'GOOSE', 1], ['EAST'], ['DROP'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['PASS'], ['FEED']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'MELON'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['BUILD_COOP'], ['NORTH'], ['PICKUP', 'GOOSE', 1], ['PASS'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['BUILD_COOP'], 'hands': [['WATER'], ['PLANT', 'MELON'], ['NORTH'], ['WATER'], ['PLACE', 'GOOSE', 1], ['EAST'], ['EAST'], ['PASS'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['EAST'], ['WATER'], ['EAST'], ['WEST'], ['WEST'], ['EAST'], ['NORTH'], ['PASS'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'MELON'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['BUILD_COOP'], ['EAST'], ['PASS'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['BUILD_COOP'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLACE', 'GOOSE', 1], ['EAST'], ['PASS'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['PASS'], ['PLACE', 'GOOSE', 1], ['WEST'], ['CARE'], ['NORTH'], ['BUILD_COOP'], ['PASS'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PASS'], ['PLANT', 'WHEAT'], ['PASS'], ['PLANT', 'WHEAT'], ['PLACE', 'GOOSE', 1], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['CARE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['HIRE']]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['EAST'], ['FEED'], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['DROP'], ['FEED'], ['WEST'], ['SOUTH'], ['CARE']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['CARE'], ['WATER'], ['DROP'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['NORTH'], ['WATER'], ['FEED'], ['WATER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['FEED'], ['NORTH'], ['CARE'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['PASS'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['DROP'], ['PASS'], ['SOUTH'], ['PASS'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PLACE', 'FERTILIZER', 2], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['SOUTH'], ['DROP'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['CARE'], ['CARE'], ['SOUTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['BUY_LAND'], []]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['NORTH'], ['CARE'], ['NORTH'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['SOUTH'], ['DROP'], ['EAST'], ['NORTH'], ['WATER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['EAST'], ['WEST'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WATER'], ['FEED'], ['BUILD_COOP'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['PLACE', 'GOOSE', 1], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['BUILD_COOP'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['SOUTH'], ['PLACE', 'GOOSE', 1], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT'], ['CARE'], ['SOUTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['CARE'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['WATER'], ['NORTH'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['CARE'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['PICKUP', 'SHEEP', 1], ['NORTH'], ['WEST'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['CARE'], ['BUILD_PASTURE'], ['NORTH'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['DROP']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['NORTH'], ['PLACE', 'SHEEP', 1], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP'], ['NORTH'], ['WEST'], ['PICKUP', 'SHEEP', 1]], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'SHEEP', 1], []]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'SHEEP', 1], ['CARE'], ['FEED'], ['NORTH'], ['EAST'], ['NORTH'], ['PICKUP', 'SHEEP', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['NORTH'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'SHEEP', 1], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['CARE'], ['WEST'], ['EAST'], ['EAST'], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['BUILD_PASTURE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'SHEEP', 1], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP'], ['CARE'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['BUILD_PASTURE'], ['HARVEST'], ['WATER'], ['BUILD_PASTURE']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['PLACE', 'SHEEP', 1], ['WEST'], ['SOUTH'], ['PLACE', 'SHEEP', 1]], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['WATER'], ['CARE'], ['FEED'], ['WATER'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 4]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['EAST'], ['NORTH'], ['CARE'], ['WEST'], ['SOUTH'], ['CARE'], ['EAST'], ['NORTH']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['CARE'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['BUILD_PASTURE']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['SOUTH'], ['CARE'], ['HARVEST'], ['NORTH'], ['CARE'], ['PASS'], ['EAST'], ['NORTH'], ['PLACE', 'SHEEP', 1]], 'market': [[]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['FEED'], ['EAST'], ['PLANT', 'WHEAT'], ['FEED'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['CARE']], 'market': [[], []]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['DROP'], ['WATER'], ['CARE'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH']], 'market': [[], []]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WATER'], ['SOUTH'], ['FEED'], ['SOUTH'], ['FEED'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 4], []]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['EAST'], ['SOUTH'], ['CARE'], ['DROP'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PASS'], ['WEST'], ['WEST'], ['EAST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['SOUTH'], ['PASS'], ['WEST'], ['PASS'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['DROP'], ['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['HARVEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['DROP'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED']], 'market': [['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['CARE'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['DROP'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['EAST'], ['NORTH'], ['FEED'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'SHEEP', 1], 'hands': [['EAST'], ['FEED'], ['CARE'], ['FEED'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['EAST'], ['FEED'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['EAST'], ['EAST'], ['WATER'], ['DROP'], ['CARE'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'MELON', 12], ['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['DROP'], ['EAST'], ['NORTH'], ['PICKUP', 'SHEEP', 1], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6], ['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['FEED'], ['EAST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP'], ['HARVEST'], ['NORTH'], ['NORTH'], ['DROP'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 6], ['SELL', 'MELON', 6]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['PLANT', 'WHEAT'], ['BUILD_PASTURE'], ['FEED'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['WATER'], ['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['FEED'], ['WATER'], ['WEST'], ['WEST'], ['FEED'], ['CARE'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['CARE'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['HARVEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['FEED'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['CARE'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['CARE'], ['HARVEST'], ['CARE'], ['SOUTH'], ['WATER'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['FEED'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['EAST'], ['CARE'], ['FEED'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['CARE'], ['SOUTH'], ['FEED'], ['WATER'], ['WATER'], ['EAST'], ['FEED'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['CARE'], ['FEED'], ['NORTH'], ['SOUTH'], ['CARE'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['DROP'], ['HARVEST'], ['WATER'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'MELON', 6], ['SELL', 'MILK', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['EAST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['CARE'], ['FERTILIZE'], ['CARE'], ['WEST'], ['FEED'], ['WEST'], ['WEST'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['EAST'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['EAST'], ['CARE'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['EAST'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['NORTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['CARE'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['HARVEST'], ['DIG'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['DROP'], 'hands': [['PASS'], ['WATER'], ['EAST'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['EAST'], ['WATER'], ['PASS'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 14], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MELON', 6], ['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['FERTILIZE'], ['WATER'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['CARE'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['PLANT', 'CARROT'], ['WEST'], ['EAST'], ['HARVEST'], ['EAST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['EAST'], ['DROP'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['FEED'], ['EAST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['DROP'], ['WEST'], ['EAST'], ['PLANT', 'CARROT'], ['EAST'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['DROP'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['DROP'], ['DROP'], ['CARE']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['FEED'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['HARVEST'], ['WEST'], ['DROP'], ['PASS'], ['CARE']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'EGG', 8], ['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['CARE'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['FEED'], ['EAST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['NORTH'], ['CARE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['CARE'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['FEED'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['CARE'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['FERTILIZE'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['WATER'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FERTILIZE'], ['NORTH'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['FEED'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['FEED'], ['NORTH'], ['WEST'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['WATER'], ['PLANT', 'CARROT'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['DROP'], ['EAST'], ['PASS'], ['HARVEST'], ['PASS']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'WHEAT', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['NORTH'], ['FEED'], ['EAST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['FEED']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['SOUTH'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['HARVEST'], ['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['HARVEST'], ['FEED'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['FEED'], ['WATER'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['CARE'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['CARE'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['DROP'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['SOUTH'], ['HARVEST'], ['FEED'], ['PLANT', 'CARROT'], ['SOUTH'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'CARROT', 2]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['HARVEST'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['DROP'], ['SOUTH'], ['WEST'], ['EAST'], ['HARVEST'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'WOOL', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['FEED'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['EAST'], ['EAST'], ['DROP'], ['SOUTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 10]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['NORTH'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['CARE'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP'], ['EAST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['FEED'], ['EAST'], ['FEED']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['DROP'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['CARE']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['FEED'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['SOUTH'], ['CARE'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['FEED'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['FEED'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['CARE'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['CARE'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST'], ['PLANT', 'CARROT'], ['NORTH'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WATER'], ['EAST'], ['EAST'], ['PLANT', 'CARROT'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['EAST'], ['PLANT', 'CARROT'], ['DROP'], ['EAST'], ['WEST'], ['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['EAST'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['FEED'], ['FEED'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'CARROT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['WEST'], ['PASS'], ['PASS'], ['CARE'], ['CARE'], ['EAST'], ['WATER'], ['DROP'], ['SOUTH'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['FEED'], ['DROP'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['SOUTH'], ['FEED'], ['CARE'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['WEST'], ['EAST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['DROP'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'MELON', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['DROP'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['DROP'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['CARE'], ['WEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['FEED'], ['SOUTH'], ['NORTH'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['CARE'], ['DROP'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['HARVEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['CARE'], ['EAST'], ['PLANT', 'CARROT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['CARE'], ['NORTH'], ['FEED'], ['EAST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['EAST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['FEED'], ['EAST'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'CARROT', 5], ['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['HARVEST'], ['CARE'], ['EAST'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['FEED'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['CARE'], ['EAST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['CARE'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['PLANT', 'CARROT'], ['WEST'], ['FERTILIZE'], ['EAST'], ['CARE']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['NORTH'], ['PLANT', 'CARROT'], ['WEST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['SOUTH'], ['DROP'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'CARROT', 8]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['PASS'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['DIG'], ['PASS'], ['EAST']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['PLACE', 'MILK', 6], ['DROP'], ['DROP'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['PLACE', 'WOOL', 4], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['EAST'], ['CARE'], ['CARE'], ['WATER'], ['EAST'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FERTILIZE'], ['WEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WATER'], ['FEED'], ['FERTILIZE'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['CARE'], ['WATER'], ['HARVEST'], ['DIG'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['WATER'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['NORTH'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['DIG'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['DIG'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['EAST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['PLANT', 'CARROT'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'CARROT'], ['EAST'], ['NORTH'], ['EAST'], ['WATER'], ['FEED'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'CARROT'], ['NORTH'], ['CARE'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['HARVEST'], ['DROP'], ['DROP']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['WATER'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['PASS'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'CARROT', 4], ['SELL', 'WHEAT', 13]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'EGG', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 6]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['HARVEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['FEED'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['HARVEST'], ['CARE'], ['NORTH'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST'], ['NORTH'], ['DIG'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['FERTILIZE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['FEED'], ['CARE'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'CARROT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['DIG'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['WATER'], ['EAST'], ['DIG']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FERTILIZE'], ['WATER'], ['EAST'], ['EAST'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['FERTILIZE'], ['PLANT', 'CARROT']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['CARE'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['PLANT', 'CARROT'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['DIG'], 'hands': [['PASS'], ['EAST'], ['DROP'], ['HARVEST'], ['FEED'], ['FERTILIZE'], ['FERTILIZE'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'CARROT', 7], ['SELL', 'EGG', 4]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 3], ['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['DIG'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['FEED'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['CARE'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['FEED']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['FEED'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['FEED'], ['FERTILIZE'], ['FEED']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FERTILIZE'], ['NORTH'], ['DIG'], ['DROP'], ['FERTILIZE'], ['WATER'], ['CARE'], ['EAST'], ['WATER'], ['CARE']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['DIG'], 'hands': [['FERTILIZE'], ['PLANT', 'WHEAT'], ['DIG'], ['EAST'], ['NORTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'CARROT', 6], ['SELL', 'WHEAT', 5]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['DROP']], 'market': [['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['HARVEST'], ['WEST'], ['CARE'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['HARVEST'], ['FEED'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['CARE'], ['FEED'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WATER'], ['HARVEST'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['FEED'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['CARE'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['DIG'], ['WATER'], ['WEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'CARROT'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['EAST'], ['SOUTH'], ['CARE'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['COLLECT_FERTILIZER'], ['PASS'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['SOUTH'], ['FEED'], ['HARVEST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['CARE'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['NORTH'], ['CARE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['HARVEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['FEED']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['EAST'], ['CARE']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['DIG'], ['FEED'], ['EAST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['CARE']], 'market': [['SELL', 'CARROT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['DIG'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 7], ['SELL', 'EGG', 2]]}, {'farmer': ['DROP'], 'hands': [['WATER'], ['PASS'], ['DROP'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'EGG', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['FEED'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['FEED'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['CARE'], ['EAST'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['EAST'], ['FERTILIZE'], ['HARVEST'], ['FEED'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['EAST'], ['CARE'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['DROP']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WEST'], ['FEED'], ['CARE'], ['SOUTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['DROP'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['PLANT', 'WHEAT'], ['DROP']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['HARVEST'], ['NORTH'], ['CARE'], ['WATER'], ['EAST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['PASS'], ['WATER'], ['PASS'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['PASS']], 'market': [['SELL', 'WHEAT', 4], ['SELL', 'EGG', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['FERTILIZE'], ['FEED'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['FEED'], ['WATER'], ['FEED']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FERTILIZE'], ['CARE'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['HARVEST'], ['EAST'], ['FEED'], ['WATER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['DROP'], ['WATER'], ['WEST'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['EAST'], ['CARE'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['PLANT', 'CARROT'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['EAST'], ['DROP'], ['PLANT', 'CARROT'], ['NORTH'], ['EAST'], ['FEED'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['HARVEST'], ['DROP'], ['EAST'], ['PASS'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['CARE'], ['EAST'], ['DROP']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['PASS'], ['EAST'], ['PASS'], ['EAST'], ['WATER'], ['SOUTH'], ['PASS'], ['EAST'], ['PASS']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['EAST'], ['PICKUP', 'FERTILIZER', 4], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'CARROT', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PLACE', 'WOOL', 4], ['WEST'], ['PLACE', 'MILK', 6], ['WATER'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['FEED'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['WEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['HARVEST'], ['CARE'], ['NORTH'], ['CARE'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['SOUTH'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['FEED'], ['EAST'], ['PLANT', 'WHEAT'], ['FEED']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['HARVEST'], ['CARE'], ['FERTILIZE'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['FEED']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['DROP'], ['EAST'], ['FEED'], ['WEST'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'MILK', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['CARE'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['DROP'], ['FERTILIZE'], ['SOUTH'], ['PASS'], ['FERTILIZE'], ['PASS'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'FERTILIZER', 3], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'EGG', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['FEED'], ['WEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['DIG'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['NORTH'], ['DIG'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['CARE'], ['SOUTH'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['DIG'], ['FERTILIZE'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['CARE'], ['EAST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['CARE'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['EAST'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['FEED'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['CARE'], ['FERTILIZE'], ['WEST'], ['FEED'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['CARE'], ['FERTILIZE'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['EAST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['DROP'], ['NORTH'], ['WATER'], ['FEED'], ['SOUTH'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['SOUTH'], ['EAST'], ['DROP'], ['EAST'], ['EAST'], ['FERTILIZE'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['FERTILIZE'], ['PASS'], ['EAST'], ['PASS'], ['PASS'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 20], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['HARVEST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['SOUTH'], ['CARE'], ['WATER'], ['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['FEED'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['CARE'], ['FEED'], ['SOUTH'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['EAST'], ['CARE'], ['SOUTH'], ['EAST'], ['HARVEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['EAST'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['EAST'], ['FEED'], ['DROP']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['EAST'], ['DROP'], ['WATER'], ['WATER'], ['SOUTH'], ['CARE'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['DROP'], ['WEST'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['NORTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['CARE'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['DROP'], ['WATER'], ['NORTH'], ['NORTH'], ['DROP'], ['EAST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['PASS'], ['NORTH'], ['HARVEST'], ['PASS'], ['PASS'], ['DROP']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'CARROT', 20], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2], ['SELL', 'EGG', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['NORTH'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FERTILIZE'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST'], ['FEED']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FERTILIZE'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WATER'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['FEED']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['EAST'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH'], ['EAST'], ['EAST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['EAST'], ['DROP'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['NORTH'], ['DROP'], ['EAST'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['NORTH'], ['PASS'], ['EAST'], ['HARVEST'], ['DROP'], ['DROP'], ['SOUTH'], ['DROP']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['HARVEST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['EAST'], ['SOUTH'], ['PASS'], ['PASS'], ['DROP'], ['PASS']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'WHEAT', 37], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MILK', 5], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['DROP'], ['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['DROP'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['DROP'], ['EAST'], ['NORTH'], ['DROP'], ['WEST'], ['NORTH'], ['WEST'], ['DROP']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['PASS'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'CARROT', 7], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['NORTH'], ['DROP'], ['EAST'], ['NORTH'], ['SOUTH'], ['PASS'], ['DROP'], ['NORTH']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['PASS'], 'hands': [['DROP'], ['NORTH'], ['PASS'], ['EAST'], ['NORTH'], ['DROP'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['HARVEST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4]]}, {'farmer': ['DROP'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['EAST'], ['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'WHEAT', 13], ['SELL', 'WHEAT', 13]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['DROP'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['EAST']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
