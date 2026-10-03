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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['NORTH'], ['PLACE', 'SHEEP']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP'], ['BUILD_PASTURE'], ['PASS'], ['CARE']], 'market': [['BUY_PRODUCT', 'WHEAT', 1], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['PLACE', 'SHEEP'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WEST'], ['BUILD_PASTURE'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 1], ['NORTH'], ['PLACE', 'COW'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PLANT', 'MELON'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'MELON'], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['FEED'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 5]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['PLANT', 'MELON'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['PASS'], ['WEST'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PASS'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['PLACE', 'FERTILIZER', 1]], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['EAST'], 'hands': [['PLACE', 'FERTILIZER', 1], ['EAST'], ['PASS'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PICKUP', 'WHEAT', 2], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WEST'], ['PASS'], ['PASS'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['PASS'], ['WEST'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLANT', 'MELON'], ['PASS'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PLANT', 'WHEAT'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['PASS'], ['WEST'], ['CARE'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['PASS'], ['NORTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 2], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 1], ['PASS'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 4], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PASS'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['PASS'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PASS'], ['HARVEST'], ['PASS'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PLANT', 'STRAWBERRY']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['HARVEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PASS'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PASS'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['PASS'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['FEED'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['PLANT', 'STRAWBERRY']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'FERTILIZER', 2], ['FEED'], ['PASS'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['PASS'], ['PASS'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WEST'], ['PASS'], ['PASS'], ['WEST'], ['PLANT', 'STRAWBERRY']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['WEST'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WATER'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['PASS'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PLACE', 'FERTILIZER', 2], ['WEST'], ['WATER'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 2], 'hands': [['PASS'], ['WATER'], ['SOUTH'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WEST'], ['SOUTH'], ['PASS'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['NORTH'], ['SOUTH'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['SOUTH'], ['PASS'], ['FEED']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['BUY_PRODUCT', 'WHEAT', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['CARE'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['PASS'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['PASS'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PASS'], ['NORTH'], ['PASS'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['PASS'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['PASS'], ['COLLECT_FERTILIZER'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['PASS'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['PASS'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PLACE', 'FERTILIZER', 1], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['BUY_PRODUCT', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 1], ['PICKUP', 'WHEAT', 1], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['NORTH'], ['FEED'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 10], 'hands': [['EAST'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['DROP'], ['WATER'], ['EAST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1]], 'market': [['SELL', 'WOOL', 6], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'COW', 1], ['COLLECT_FERTILIZER'], ['PASS'], ['PASS'], ['EAST'], ['NORTH'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['PICKUP', 'WHEAT', 1], ['PICKUP', 'WHEAT', 1], ['WATER'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 1]], 'market': [['BUY_SEED', 'WHEAT', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['PICKUP', 'GOOSE', 1], ['PASS'], ['EAST'], ['NORTH'], ['WATER'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['PLACE', 'COW'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'GOOSE', 1], ['PASS'], ['EAST'], ['FEED'], ['WATER'], ['EAST'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'COW', 1], ['BUILD_COOP'], ['CARE'], ['EAST'], ['EAST'], ['WEST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['PLACE', 'GOOSE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['PICKUP', 'GOOSE', 1]], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['EAST'], 'hands': [['BUILD_COOP'], ['NORTH'], ['WEST'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 3], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'GOOSE'], ['BUILD_PASTURE'], ['PICKUP', 'COW', 1], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['PLACE', 'COW'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'TOMATO'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['BUILD_COOP']], 'market': [['BUY_SEED', 'WHEAT', 3], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'CARROT'], ['PICKUP', 'COW', 1], ['NORTH'], ['PLACE', 'GOOSE'], ['EAST'], ['EAST'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['NORTH'], ['BUILD_PASTURE'], ['EAST'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['NORTH'], ['PLACE', 'COW'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['BUILD_COOP']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'CARROT'], ['BUILD_PASTURE'], ['CARE'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER'], ['PLACE', 'GOOSE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WATER'], ['PLACE', 'COW'], ['SOUTH'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 10], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['WEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['WEST'], ['CARE'], ['WEST'], ['EAST'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 3], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['FEED'], ['WATER'], ['SOUTH'], ['PASS'], ['PLACE', 'FERTILIZER', 1]], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['PASS'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_PRODUCT', 'WHEAT', 3], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['CARE'], ['PICKUP', 'GOOSE', 1], ['EAST'], ['FEED'], ['WATER'], ['EAST'], ['PLANT', 'CARROT'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['CARE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PICKUP', 'WHEAT', 3]], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['CARE'], ['EAST'], ['SOUTH'], ['FEED'], ['EAST'], ['SOUTH'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['EAST'], ['NORTH'], ['SOUTH'], ['EAST'], ['WATER'], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['BUILD_COOP'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['PASS'], ['PLANT', 'WHEAT'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['PLACE', 'GOOSE'], ['WATER'], ['NORTH'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['PASS'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['PASS'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['PASS'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 6], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['BUY_PRODUCT', 'WHEAT', 13], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 4]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['SOUTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'WHEAT', 4]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 2], 'hands': [['PLANT', 'WHEAT'], ['FEED'], ['FEED'], ['PASS'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PASS'], ['CARE'], ['PASS'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['NORTH'], ['PASS'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['WEST'], ['PASS'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['HARVEST'], ['PASS'], ['COLLECT_FERTILIZER'], ['PASS'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'TOMATO'], ['PASS'], ['EAST'], ['PASS'], ['WATER'], ['WATER'], ['HARVEST'], ['PLANT', 'CARROT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['EAST'], ['PASS'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['HARVEST'], ['PASS'], ['FEED'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PLANT', 'CARROT'], ['PASS'], ['CARE'], ['WATER'], ['WEST'], ['HARVEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PLANT', 'TOMATO'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 7], ['BUY_ANIMAL', 'COW', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'COW', 1], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3]], 'market': [['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PLACE', 'COW', 1], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': []}, {'farmer': ['PLACE', 'WOOL', 4], 'hands': [['EAST'], ['PICKUP', 'COW', 1], ['WEST'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['EAST'], ['CARE'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['BUY_LAND']]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['DROP'], ['SOUTH'], ['FEED'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['FEED'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['CARE'], ['NORTH'], ['EAST'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 1], ['BUILD_PASTURE'], ['FEED'], ['NORTH'], ['NORTH'], ['DROP'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PLACE', 'COW'], ['CARE'], ['FEED'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['CARE'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'COW', 1], ['PLANT', 'CARROT'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['CARE'], ['FEED'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'TOMATO', 1], []]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['PLANT', 'TOMATO'], ['EAST'], ['FEED'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLACE', 'COW'], ['PLANT', 'CARROT'], ['WATER'], ['CARE'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PICKUP', 'GOOSE', 1], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 2], 'hands': [['WEST'], ['SOUTH'], ['PLANT', 'TOMATO'], ['EAST'], ['HARVEST'], ['BUILD_COOP'], ['PLANT', 'TOMATO'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['SOUTH'], ['PLANT', 'CARROT'], ['PLACE', 'GOOSE'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['BUILD_COOP'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 2], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLACE', 'GOOSE'], ['SOUTH'], ['PLANT', 'TOMATO'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['PLANT', 'TOMATO'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['BUILD_COOP'], 'hands': [['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE'], 'hands': [['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['SOUTH'], ['PLANT', 'TOMATO'], ['WATER'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 7], ['BUY_PRODUCT', 'WHEAT', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['WEST'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['CARE'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['DROP'], ['SOUTH'], ['DROP'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MELON', 12]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['FEED'], ['CARE'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 15], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['CARE'], ['EAST'], ['EAST'], ['NORTH'], ['WEST'], ['DROP'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['DROP'], ['WATER'], ['FEED'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['SOUTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_LAND']]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['EAST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['CARE'], ['WEST'], ['WEST'], ['EAST'], ['WATER'], ['DROP']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['CARE'], ['FEED'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 5], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['NORTH'], ['FEED'], ['CARE'], ['EAST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['EAST'], ['EAST'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['DROP'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'CARROT', 6], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['FEED'], ['BUILD_COOP'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['CARE'], ['PLACE', 'GOOSE'], ['WEST'], ['WATER'], ['PLANT', 'CARROT']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['FEED'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WEST'], ['WEST'], ['CARE'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'CARROT', 9]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 14], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 4], ['BUY_PRODUCT', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['HARVEST'], ['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['FEED'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['CARE'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WATER'], ['HARVEST'], ['DROP'], ['FEED'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['SELL', 'WHEAT', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['SOUTH'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['CARE'], ['WATER'], ['EAST'], ['SOUTH'], ['FEED'], ['EAST'], ['FEED']], 'market': [['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['CARE'], ['EAST'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['BUILD_COOP'], ['NORTH'], ['SOUTH'], ['NORTH'], ['FEED'], ['FERTILIZE'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['CARE'], ['PLACE', 'GOOSE'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['SOUTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['FEED'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'TOMATO'], ['WEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['NORTH'], ['FEED'], ['SOUTH'], ['EAST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['CARE'], ['PLANT', 'CARROT'], ['SOUTH'], ['PLANT', 'CARROT'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'MELON', 6], ['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['WATER'], ['PASS'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_PRODUCT', 'WHEAT', 13], ['SELL', 'EGG', 8], ['BUY_SEED', 'TOMATO', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['CARE'], ['CARE'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['PLANT', 'CARROT'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['WATER'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['CARE'], ['WATER'], ['NORTH'], ['FEED'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['SOUTH'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['EAST'], ['WEST'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['HARVEST'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'CARROT', 6], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['EAST'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['PLANT', 'TOMATO'], ['PLANT', 'CARROT'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['EAST'], ['EAST'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['CARE'], ['WATER'], ['SOUTH'], ['HARVEST'], ['PLANT', 'TOMATO'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'TOMATO'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['PLANT', 'TOMATO'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 1], ['SELL', 'CARROT', 12], ['SELL', 'EGG', 4]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'EGG', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 14], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['WATER'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WATER'], ['CARE'], ['HARVEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['PLANT', 'CARROT'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WATER'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['CARE'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['CARE'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['PLANT', 'CARROT'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['EAST'], ['HARVEST'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['HARVEST'], ['EAST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['PLANT', 'TOMATO'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['FEED'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['NORTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 7], ['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'CARROT', 12]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 14], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PLACE', 'MILK', 6], ['FEED'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['PLACE', 'MILK', 6], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['HARVEST'], ['FEED']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['EAST'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['WATER'], ['HARVEST'], ['CARE'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['PLACE', 'MILK', 3], ['NORTH'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['DROP'], ['FEED']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['CARE'], ['WEST'], ['FEED'], ['NORTH'], ['FEED'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['WATER'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['FEED'], ['PLANT', 'WHEAT'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['CARE'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['FERTILIZE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['FEED'], ['FEED'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['EAST'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['HARVEST'], ['FEED'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['EAST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['DROP'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['SOUTH'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3], ['SELL', 'WHEAT', 1], ['SELL', 'CARROT', 9], ['SELL', 'EGG', 10]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'CARROT', 1], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'EGG', 4], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['WATER'], ['CARE'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['NORTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['FEED'], ['WATER'], ['SOUTH'], ['FEED'], ['FEED'], ['DIG'], ['WEST'], ['CARE'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['HARVEST'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['CARE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'CARROT'], ['NORTH'], ['WATER'], ['WATER'], ['FEED'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['FEED'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['DROP'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 4], ['SELL', 'CARROT', 8], ['SELL', 'TOMATO', 2], ['SELL', 'EGG', 10]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['PASS'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'FERTILIZER', 1], ['SELL', 'WHEAT', 4]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PLACE', 'MILK', 3], ['FEED'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'MILK', 3], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['WATER'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLACE', 'MILK', 3], ['HARVEST'], ['WATER'], ['WEST'], ['FEED'], ['HARVEST'], ['FEED'], ['EAST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['PLANT', 'CARROT'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'TOMATO'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['SOUTH'], ['HARVEST'], ['FEED'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['FEED'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['PLANT', 'TOMATO'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['WEST'], ['HARVEST'], ['CARE'], ['SOUTH'], ['WATER'], ['CARE'], ['CARE'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'TOMATO'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['SELL', 'CARROT', 13]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['PLANT', 'TOMATO'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['SOUTH'], ['PLANT', 'TOMATO'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['PLANT', 'TOMATO'], ['NORTH'], ['WEST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 2], ['SELL', 'CARROT', 2], ['SELL', 'TOMATO', 2], ['SELL', 'EGG', 15]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['PASS'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PLACE', 'MILK', 6], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['CARE'], ['EAST'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['CARE'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['PLANT', 'TOMATO'], ['NORTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['FEED'], ['FERTILIZE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['WATER'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['FEED'], ['SOUTH'], ['HARVEST'], ['CARE'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['CARE'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['SOUTH'], ['EAST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['FEED'], ['PLANT', 'TOMATO'], ['WATER'], ['FEED'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['CARE'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['CARE'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['EAST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['CARE'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['FEED'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['CARE'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['DIG'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['DROP'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'TOMATO'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'CARROT', 9], ['SELL', 'TOMATO', 6], ['SELL', 'EGG', 16]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'WHEAT', 3], ['SELL', 'CARROT', 4], ['SELL', 'EGG', 7]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'CARROT'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['FEED'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'TOMATO'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['CARE']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'TOMATO'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['FEED'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['WATER'], ['PLANT', 'TOMATO'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'TOMATO'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['FEED'], ['FERTILIZE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['PLANT', 'TOMATO'], ['NORTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['WATER'], ['CARE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['DIG'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['DIG'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['DIG'], 'hands': [['EAST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 4], ['SELL', 'TOMATO', 13], ['SELL', 'EGG', 10]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'TOMATO', 1], ['SELL', 'EGG', 9]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['SOUTH'], ['PLACE', 'MILK', 3], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2]], 'market': [['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['PLANT', 'CARROT'], ['CARE'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['CARE'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['WATER'], ['FEED'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['FEED'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['SOUTH'], ['CARE'], ['NORTH'], ['HARVEST'], ['FEED'], ['NORTH'], ['EAST'], ['CARE'], ['FEED'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'TOMATO', 10]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['CARE'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['DIG'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['DIG'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['DIG'], ['PLANT', 'CARROT'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['WEST']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'TOMATO'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['FEED']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['CARE']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['DIG'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['EAST'], ['DIG'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['DIG'], ['HARVEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['DIG'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PLANT', 'TOMATO'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 4], ['SELL', 'CARROT', 10], ['SELL', 'TOMATO', 6], ['SELL', 'EGG', 10]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['PASS'], ['DIG'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['SELL', 'TOMATO', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['BUY_PRODUCT', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'MILK', 5], ['FEED'], ['EAST'], ['FEED'], ['HARVEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'WHEAT', 10], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['DIG'], ['SOUTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['WEST'], ['EAST'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['CARE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['FEED'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['DIG'], 'hands': [['FEED'], ['FERTILIZE'], ['FEED'], ['WEST'], ['HARVEST'], ['DIG'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['FERTILIZE'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['DIG'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['DIG'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'MILK', 1], ['SELL', 'WHEAT', 1], ['SELL', 'CARROT', 2], ['SELL', 'TOMATO', 8], ['SELL', 'EGG', 15]]}, {'farmer': ['DIG'], 'hands': [['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'CARROT', 1], ['SELL', 'TOMATO', 1], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['SELL', 'TOMATO', 10], ['BUY_PRODUCT', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['EAST']], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['PLANT', 'CARROT'], ['CARE'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST'], ['CARE'], ['HARVEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FEED'], ['WATER'], ['FEED'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['CARE'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['SOUTH'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['NORTH'], ['WEST'], ['FEED'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['FEED'], ['FERTILIZE'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['CARE'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['PLANT', 'CARROT'], ['NORTH'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['DIG'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 1], ['SELL', 'CARROT', 2], ['SELL', 'TOMATO', 10], ['SELL', 'EGG', 5]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'TOMATO', 2], ['SELL', 'EGG', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'TOMATO', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'FERTILIZER', 3], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['WEST']], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['SOUTH'], ['PLACE', 'MILK', 6], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 5], ['SELL', 'WHEAT', 10]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['PLANT', 'CARROT'], ['CARE'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['FEED'], ['FEED'], ['FERTILIZE'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['SOUTH'], ['FEED'], ['PLANT', 'WHEAT'], ['SOUTH'], ['CARE'], ['CARE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['NORTH'], ['FEED'], ['PLANT', 'CARROT'], ['CARE'], ['FEED'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['CARE'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['FERTILIZE']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'WHEAT', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['DIG'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'CARROT', 13], ['SELL', 'TOMATO', 2], ['SELL', 'EGG', 10]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'TOMATO', 1], ['SELL', 'EGG', 9]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['PICKUP', 'FERTILIZER', 3], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 5], ['SELL', 'WHEAT', 10]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['CARE'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['FERTILIZE'], ['FEED'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['FEED']], 'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['WATER'], ['SOUTH'], ['CARE'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['PLANT', 'CARROT'], ['CARE'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['FEED'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['FERTILIZE'], ['WATER'], ['WEST'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['FEED'], ['WATER'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1], ['SELL', 'CARROT', 12]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['FERTILIZE'], ['HARVEST'], ['CARE'], ['PLANT', 'CARROT'], ['HARVEST'], ['NORTH'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['NORTH'], ['WATER'], ['DIG'], ['FEED'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'CARROT'], ['CARE'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['WEST'], ['EAST'], ['CARE'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['FEED'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['SOUTH'], ['DROP'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['CARE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PLANT', 'CARROT']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'WHEAT', 10], ['SELL', 'CARROT', 1], ['SELL', 'TOMATO', 10], ['SELL', 'EGG', 2]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['PASS'], ['PASS'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 1], ['SELL', 'TOMATO', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'CARROT', 9], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'MILK', 6], ['FEED'], ['HARVEST'], ['PLACE', 'MILK', 3], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': [['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['PLANT', 'CARROT'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['EAST'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['FEED'], ['PLANT', 'CARROT'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['FEED'], ['WATER'], ['PLANT', 'CARROT'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WATER']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['SOUTH'], ['WATER'], ['CARE'], ['EAST'], ['WATER'], ['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['EAST']], 'market': [['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['FEED'], ['WATER'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['NORTH'], ['FERTILIZE'], ['EAST'], ['PLANT', 'CARROT'], ['DIG'], ['PLANT', 'CARROT'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['HARVEST'], ['DIG'], ['NORTH'], ['WATER'], ['SOUTH'], ['CARE'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['DIG'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WEST'], ['HARVEST'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['NORTH'], ['WATER'], ['PASS'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'CARROT', 13], ['SELL', 'TOMATO', 7], ['SELL', 'EGG', 10]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PASS'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'EGG', 7]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'FERTILIZER', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'CARROT', 9], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'CARROT'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['FEED'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['CARE'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['CARE'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['FEED'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['FEED'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['FEED'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['WATER'], ['CARE'], ['EAST'], ['CARE'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['DIG'], ['EAST'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['FEED'], ['WATER'], ['SOUTH'], ['DIG'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['PLANT', 'CARROT'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['SOUTH'], ['WATER'], ['WEST'], ['FEED'], ['SOUTH'], ['EAST'], ['CARE'], ['EAST'], ['DROP'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['CARE'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['DIG'], ['EAST'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 6]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['EAST'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['EAST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['DIG'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 4]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['WATER'], ['EAST'], ['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['DROP'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 1], ['SELL', 'CARROT', 6], ['SELL', 'TOMATO', 13], ['SELL', 'EGG', 10]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['PASS'], ['HARVEST'], ['SOUTH'], ['PASS'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'WHEAT', 3], ['SELL', 'CARROT', 2], ['SELL', 'TOMATO', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['SELL', 'TOMATO', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST']], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['PLACE', 'MILK', 3], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 4], ['BUY_SEED', 'WHEAT', 1], ['SELL', 'CARROT', 9]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['WATER'], ['EAST'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['DIG'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['NORTH'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'CARROT', 6], ['SELL', 'EGG', 8]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WEST'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FERTILIZE'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'TOMATO', 6]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['DROP'], ['EAST'], ['WEST'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 2], ['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['DROP'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['SELL', 'TOMATO', 5], ['SELL', 'EGG', 4]]}, {'farmer': ['SOUTH'], 'hands': [['DIG'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 1], ['SELL', 'WHEAT', 4], ['SELL', 'CARROT', 7], ['SELL', 'TOMATO', 2], ['SELL', 'EGG', 1]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST']], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['PLACE', 'MILK', 2], ['HARVEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['PLANT', 'CARROT'], ['NORTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['EAST'], ['DIG'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['CARE'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['DIG'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['FEED'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'CARROT', 9]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['CARE'], ['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['DROP'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'TOMATO', 10]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['SOUTH'], ['DROP'], ['SOUTH'], ['FEED'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['FERTILIZE'], ['EAST'], ['PASS'], ['WEST'], ['HARVEST'], ['CARE'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 6]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 1], ['SELL', 'TOMATO', 10]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['FEED'], ['FERTILIZE'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 4]]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3], ['SELL', 'CARROT', 2], ['SELL', 'TOMATO', 6], ['SELL', 'EGG', 8]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['FEED'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'CARROT', 7], ['SELL', 'TOMATO', 2]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'CARROT', 16], ['SELL', 'TOMATO', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 2], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'MILK', 5], ['SELL', 'CARROT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'CARROT', 3]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2], ['SELL', 'EGG', 10]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['FEED'], ['EAST'], ['NORTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['CARE'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['DROP'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['HARVEST'], ['DROP'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 11], ['SELL', 'TOMATO', 10]]}, {'farmer': ['EAST'], 'hands': [['DROP'], ['HARVEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['DROP'], ['WEST'], ['WATER'], ['WEST'], ['PASS']], 'market': [['SELL', 'CARROT', 4], ['SELL', 'EGG', 6]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['DROP'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'TOMATO', 2]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['EAST'], ['SOUTH'], ['PASS'], ['WEST'], ['EAST'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['EAST'], ['DROP'], ['SOUTH'], ['PASS'], ['DROP'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'WHEAT', 11], ['SELL', 'TOMATO', 6], ['SELL', 'EGG', 6]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['PASS'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'WHEAT', 2], ['SELL', 'CARROT', 11], ['SELL', 'TOMATO', 4], ['SELL', 'EGG', 2]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['SELL', 'CARROT', 16], ['SELL', 'WHEAT', 7], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['HIRE'], ['HIRE'], ['SELL', 'STRAWBERRY', 2], ['SELL', 'CARROT', 4]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['DROP'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['DROP'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'WHEAT', 4], ['SELL', 'MILK', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['DROP'], ['WEST'], ['SOUTH'], ['WEST'], ['DROP'], ['NORTH'], ['EAST']], 'market': [['SELL', 'CARROT', 3], ['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 3], ['SELL', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WEST'], ['DROP']], 'market': [['SELL', 'WHEAT', 4], ['SELL', 'CARROT', 4], ['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['PASS'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 1], ['SELL', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['DROP'], ['EAST'], ['WEST'], ['PASS'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 1], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['DROP'], ['DROP'], ['PASS'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['PASS'], ['WEST'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 5], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WEST'], ['SOUTH'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'TOMATO', 3], ['SELL', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'EGG', 12], ['SELL', 'CARROT', 8], ['SELL', 'MILK', 1]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
