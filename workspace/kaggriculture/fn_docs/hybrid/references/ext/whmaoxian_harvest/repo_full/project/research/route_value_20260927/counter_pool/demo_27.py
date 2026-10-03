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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PICKUP', 'SHEEP', 1], ['NORTH'], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1]], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['BUILD_PASTURE'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['SOUTH'], ['BUILD_PASTURE']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['DIG'], ['WEST'], ['SOUTH']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['PICKUP', 'COW', 1], ['SOUTH'], ['PLACE', 'COW', 1], ['WEST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['SOUTH'], 'hands': [['DIG'], ['PLACE', 'COW', 1], ['SOUTH'], ['CARE'], ['BUILD_PASTURE']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['CARE'], ['CARE'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['PICKUP', 'SHEEP', 1], 'hands': [['WATER'], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PLANT', 'MELON']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['WATER']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 1], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['WATER'], ['WEST'], ['WEST'], ['WEST'], ['PLANT', 'MELON']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['BUILD_PASTURE'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'MELON'], ['WATER'], ['PLACE', 'COW', 1], ['FEED'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PLANT', 'MELON'], ['WEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [[]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['PASS'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], [], []]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['DROP'], ['DROP'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['WEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['PLANT', 'MELON'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['EAST'], ['EAST'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], []]}, {'farmer': ['PICKUP', 'WHEAT', 1], 'hands': [['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 2], ['EAST'], ['SOUTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['DROP'], ['DROP'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['PICKUP', 'COW', 1], ['PICKUP', 'COW', 1], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['WATER'], ['HARVEST']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['BUILD_PASTURE'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['PLACE', 'COW', 1], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], [], []]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['DROP'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WATER'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['CARE'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['CARE'], ['DROP']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['WATER'], ['CARE'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['FEED'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [['DROP'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['BUILD_PASTURE'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': [[]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['WEST']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['PASS'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['DROP'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WATER'], ['DROP'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['WATER'], ['WEST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['HARVEST'], ['WEST'], ['WATER'], ['DROP']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['FEED'], ['WATER'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['EAST'], ['DROP'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['EAST'], ['PICKUP', 'WHEAT', 1], ['HARVEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['WEST'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['DROP'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WEST'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WATER'], ['CARE'], ['WATER'], ['EAST']], 'market': [[]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WEST'], ['EAST']], 'market': [[]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['WATER'], ['DROP']], 'market': [[]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [[]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['CARE'], ['WATER'], ['WEST']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [[]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PASS'], ['WEST']], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [[]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['DROP'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'GOOSE', 1], ['DROP'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['EAST'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'STRAWBERRY'], ['CARE'], ['DROP'], ['BUILD_COOP'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WEST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'GOOSE', 1], ['PLACE', 'GOOSE', 1], ['NORTH'], ['WATER'], ['WATER'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 3]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['DROP'], ['BUILD_COOP'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['PICKUP', 'GOOSE', 1], ['PLACE', 'GOOSE', 1], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['BUILD_COOP'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['PLACE', 'GOOSE', 1], ['EAST']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['DROP']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['BUILD_COOP'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['PASS'], ['WATER'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 1]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['PLACE', 'GOOSE', 1], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['EAST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH'], ['PASS'], ['PASS'], ['CARE']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['WATER'], ['WEST'], ['PASS'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], []]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [[], [], []]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['EAST'], ['NORTH']], 'market': [[], [], []]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['DROP'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['FEED'], ['WATER'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['EAST'], ['DROP'], ['CARE'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 2], ['FEED'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WATER'], ['DROP'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['PICKUP', 'WHEAT', 1], ['FEED'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['EAST'], ['WEST'], ['CARE'], ['WATER'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'GOOSE', 1], ['FEED'], ['FEED'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['WATER'], ['WATER'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['EAST'], ['EAST'], ['WEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['EAST'], ['PICKUP', 'WHEAT', 1], ['WATER'], ['WATER'], ['EAST'], ['DROP']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['PICKUP', 'WHEAT', 1]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_COOP'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'GOOSE', 1], ['WATER'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['NORTH'], ['CARE'], ['WATER'], ['WEST'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], [], []]}, {'farmer': ['HARVEST'], 'hands': [['DROP'], ['NORTH'], ['PICKUP', 'WHEAT', 1], ['NORTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [[], []]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['DROP'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['EAST'], 'hands': [['DROP'], ['CARE'], ['FEED'], ['NORTH'], ['DROP'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 6], ['BUY_LAND']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['CARE'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['DROP'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['CARE'], ['SOUTH'], ['EAST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['DROP']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['DROP'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['SOUTH'], ['PLANT', 'MELON'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['BUILD_COOP'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [[], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLACE', 'GOOSE', 1], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['PICKUP', 'WHEAT', 1], ['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], []]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [[], [], []]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [[], [], []]}, {'farmer': ['DROP'], 'hands': [['WATER'], ['CARE'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['DROP']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['WEST'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'WOOL', 4], ['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 11]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FEED'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['WATER'], ['WATER'], ['DROP'], ['NORTH'], ['SOUTH'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['WEST'], ['DROP']], 'market': [['SELL', 'WOOL', 3], ['BUY_SEED', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['NORTH'], ['FEED'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['CARE'], ['PLANT', 'WHEAT'], ['EAST'], ['CARE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['DROP']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['PICKUP', 'GOOSE', 1]], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['CARE'], ['WATER'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['BUILD_COOP']], 'market': [['SELL', 'WHEAT', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['EAST'], ['PLACE', 'GOOSE', 1]], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['WATER'], ['WATER'], ['WATER'], ['EAST'], ['FEED'], ['WATER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['BUILD_COOP'], 'hands': [['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['WEST'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['DROP'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['FEED']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['DROP'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 1], ['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 7]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['SOUTH'], ['DROP'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MELON', 6], ['SELL', 'MILK', 1], [], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['FEED'], ['WATER'], ['FEED']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['CARE'], ['EAST'], ['CARE']], 'market': [[]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['SOUTH'], ['EAST'], ['DROP'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6], [], ['BUY_PRODUCT', 'WHEAT', 11]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['DROP'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 12], ['SELL', 'MILK', 3], ['BUY_LAND']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['DROP'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['FEED']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['DROP'], ['EAST'], ['FEED'], ['WEST'], ['CARE']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['NORTH'], ['EAST'], ['FEED'], ['PICKUP', 'WHEAT', 4], ['DROP'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['CARE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['SELL', 'MILK', 3], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['EAST'], ['EAST'], ['CARE'], ['EAST'], ['EAST'], ['SOUTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['FEED'], ['EAST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['WEST'], ['PLANT', 'TOMATO'], ['FEED'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WEST'], ['WATER'], ['CARE'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['FEED'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 5], ['NORTH'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['EAST'], ['WEST'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['EAST'], ['CARE'], ['DROP'], ['WATER']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['EAST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['SOUTH'], ['FEED'], ['CARE'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['EAST'], ['WATER'], ['EAST'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['EAST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['FEED'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['CARE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['CARE'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'TOMATO'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['HARVEST'], ['FEED'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['EAST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'EGG', 12], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 20]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['PASS'], ['NORTH'], ['EAST'], ['PASS'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'MELON', 6], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['SOUTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 5], ['SELL', 'WOOL', 1]]}, {'farmer': ['DROP'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['HARVEST'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['EAST'], ['WATER'], ['FEED'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['WATER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'TOMATO'], ['EAST'], ['HARVEST'], ['CARE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['FEED'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['EAST'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['CARE'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['FEED'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['CARE'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'TOMATO'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['PASS'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 24], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['PLANT', 'TOMATO'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 10], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['EAST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 9], ['SELL', 'FERTILIZER', 4], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['FEED'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['WATER'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['EAST'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['HARVEST'], ['NORTH'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST']], 'market': [['SELL', 'EGG', 6], ['SELL', 'WHEAT', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 3], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['WATER'], ['PLANT', 'TOMATO'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'EGG', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'EGG', 5]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'TOMATO'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['EAST'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['EAST'], ['WATER'], ['WATER'], ['PASS'], ['EAST'], ['EAST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 7], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['DROP'], ['FEED'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['FEED'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 9]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['CARE'], ['WATER']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'EGG', 7], ['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'WHEAT', 9], ['SELL', 'EGG', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['DROP'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'FERTILIZER', 7], ['WEST'], ['EAST'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'MILK', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['PICKUP', 'FERTILIZER', 6], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 9], ['SELL', 'EGG', 7], ['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['DROP'], 'hands': [['FEED'], ['CARE'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['FEED'], ['PICKUP', 'SHEEP', 1]], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['BUILD_PASTURE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['FEED'], ['FEED'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['PLACE', 'SHEEP', 1], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'SHEEP', 1], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST']], 'market': [['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'SHEEP', 1], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH'], ['FEED'], ['CARE'], ['DIG'], ['BUILD_PASTURE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['CARE'], ['EAST'], ['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['EAST'], ['CARE'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['PLACE', 'SHEEP', 1], ['FEED']], 'market': [['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['FEED'], ['CARE'], ['PICKUP', 'SHEEP', 1], ['CARE']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['PLANT', 'TOMATO'], ['FERTILIZE'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['DIG'], ['FEED']], 'market': [['SELL', 'EGG', 5], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'SHEEP', 1], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['BUILD_PASTURE'], ['CARE']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['PLACE', 'SHEEP', 1], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FEED'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['HARVEST'], ['EAST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['WEST'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PASS'], ['EAST'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'EGG', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['WEST'], ['CARE'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['FEED'], ['NORTH'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['CARE'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['CARE'], ['CARE'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'SHEEP', 1]], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'MILK', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['BUILD_PASTURE'], ['FEED'], ['WEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['FEED'], ['SOUTH'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FEED'], ['FEED'], ['CARE'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['NORTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['FEED'], ['BUILD_PASTURE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['FEED'], ['EAST'], ['WATER'], ['DROP'], ['WEST'], ['DROP'], ['EAST'], ['HARVEST'], ['SOUTH'], ['CARE'], ['PLACE', 'SHEEP', 1]], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['FEED'], ['DIG'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 9]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'WHEAT', 7], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['WEST'], ['SOUTH'], ['DIG'], ['NORTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['WATER'], ['FERTILIZE'], ['PLANT', 'TOMATO'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['DROP'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'EGG', 10], ['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['DROP'], ['WEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['WEST'], ['EAST'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['PASS'], ['WEST'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 9], ['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['SELL', 'EGG', 9], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['FEED'], ['WEST'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['WEST'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['CARE'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['HARVEST'], ['EAST'], ['FEED'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['FEED'], ['WEST'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'TOMATO', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['PLANT', 'TOMATO'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['DIG'], ['WEST']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'EGG', 5]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['DIG'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['PLANT', 'TOMATO'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['EAST'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['DROP'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'TOMATO'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'EGG', 6], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['FERTILIZE'], ['EAST'], ['PASS'], ['SOUTH'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 11], ['SELL', 'STRAWBERRY', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 19], ['SELL', 'MILK', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER']], 'market': [['HIRE']]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['HARVEST'], ['CARE'], ['CARE'], ['HARVEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['DROP']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['WEST'], ['SOUTH'], ['NORTH'], ['DIG'], ['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['DROP'], ['DROP'], ['WATER'], ['HARVEST'], ['SOUTH'], ['CARE'], ['WEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 5], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['EAST'], ['PLANT', 'TOMATO'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['FEED'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['CARE'], ['PLANT', 'TOMATO'], ['WEST']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['WEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WEST'], ['PLANT', 'TOMATO'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['DROP'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['DIG'], ['WEST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 12], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['DROP'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['NORTH'], ['DROP'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['PASS'], ['HARVEST'], ['EAST'], ['WEST'], ['DROP'], ['WATER'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 7], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['NORTH'], ['PASS'], ['PASS'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 12], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 11]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['FEED'], ['HARVEST'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['CARE'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['FEED'], ['HARVEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WATER'], ['FEED'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['CARE'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['HARVEST'], ['FEED'], ['FEED'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['CARE'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['FEED'], ['NORTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'EGG', 6], ['SELL', 'WHEAT', 8]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['DROP'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 1], ['NORTH'], ['FERTILIZE'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['EAST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'EGG', 4], ['SELL', 'FERTILIZER', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['WEST'], ['DIG'], ['EAST'], ['WATER'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['EAST'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['WATER']], 'market': [['SELL', 'MELON', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['FEED'], ['FEED'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'EGG', 8], ['SELL', 'WHEAT', 9]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['DIG'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['HARVEST'], ['CARE'], ['CARE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['FEED'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'EGG', 7], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['NORTH'], ['HARVEST'], ['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['CARE'], ['SOUTH'], ['WATER'], ['DIG'], ['FERTILIZE'], ['CARE'], ['WEST'], ['WEST'], ['SOUTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['DIG'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'EGG', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FERTILIZE'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['EAST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['DIG'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['PASS'], ['NORTH'], ['PASS'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['PASS'], ['WEST'], ['PASS'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['PASS'], ['PASS'], ['FERTILIZE'], ['PASS'], ['WATER'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'WOOL', 5], ['SELL', 'MELON', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 10], ['SELL', 'TOMATO', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['EAST'], ['HARVEST'], ['DROP'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['SELL', 'WOOL', 18], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['FEED'], ['WEST'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['FEED'], ['EAST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['CARE'], ['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['FEED'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['WATER'], ['CARE'], ['FERTILIZE'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['HARVEST'], ['FEED'], ['FEED'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['CARE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['CARE'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['FEED'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 9], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FERTILIZE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['DROP'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 10], ['SELL', 'WHEAT', 12], ['SELL', 'CARROT', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['DROP'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'WHEAT', 1], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 8], ['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'WOOL', 6], ['SELL', 'STRAWBERRY', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 5]]}, {'farmer': ['PASS'], 'hands': [['CARE'], ['PASS'], ['WATER'], ['FERTILIZE'], ['PASS'], ['WEST'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['DROP'], ['FEED'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': [['HIRE']]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['SOUTH'], ['EAST'], ['FEED'], ['DIG'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['CARE'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['FEED'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['CARE'], ['DIG'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'EGG', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['WEST'], ['CARE'], ['SOUTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'WOOL', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['FEED'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['CARE'], ['DIG']], 'market': [['SELL', 'WOOL', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['CARE'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['DIG'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 14], ['SELL', 'CARROT', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['DIG'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['FERTILIZE'], ['EAST'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['DIG'], ['SOUTH'], ['DIG']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'EGG', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['DIG'], ['SOUTH'], ['NORTH'], ['DROP'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['DROP'], ['EAST'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['PASS'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['PASS'], ['PASS'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'EGG', 4], ['SELL', 'WHEAT', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'TOMATO', 10], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'FERTILIZER', 2], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['FEED'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['FEED'], ['HARVEST'], ['DIG'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['NORTH'], ['CARE'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['CARE'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['HARVEST'], ['NORTH'], ['FEED'], ['FERTILIZE'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WATER'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['FEED'], ['FEED'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['CARE'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'WHEAT', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['FEED'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['EAST'], ['FERTILIZE'], ['CARE'], ['HARVEST'], ['DIG'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 5], ['SELL', 'TOMATO', 2], ['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['HARVEST'], ['EAST'], ['EAST'], ['DROP'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WATER'], ['DROP'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['DIG'], ['PLANT', 'WHEAT'], ['WATER'], ['PICKUP', 'WHEAT', 1], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 11], ['SELL', 'EGG', 7], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'FERTILIZER', 4], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['EAST'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['WEST'], ['WEST'], ['PASS'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WOOL', 5], ['SELL', 'EGG', 3], ['SELL', 'WHEAT', 3], ['SELL', 'STRAWBERRY', 1], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['DROP'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['HARVEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'TOMATO', 4], ['SELL', 'FERTILIZER', 4], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['EAST'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['DROP']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['DIG'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 16]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['FEED'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['CARE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['EAST'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'WHEAT', 12], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['DIG'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['DROP'], ['PLANT', 'WHEAT'], ['EAST'], ['DROP'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['PASS'], ['NORTH'], ['DROP'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'WHEAT', 16], ['SELL', 'FERTILIZER', 4]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['COLLECT_FERTILIZER'], ['PASS'], ['HARVEST'], ['PASS'], ['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 4], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['PICKUP', 'FERTILIZER', 2], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['SELL', 'TOMATO', 10], ['SELL', 'FERTILIZER', 3], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['CARE'], ['FEED'], ['CARE'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['FEED'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['CARE'], ['FERTILIZE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['HARVEST'], ['EAST'], ['FEED'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['SOUTH'], ['EAST'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['FEED'], ['CARE'], ['WEST'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['EAST'], ['CARE'], ['SOUTH'], ['WATER'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['NORTH'], ['DIG'], ['DROP'], ['SOUTH'], ['SOUTH'], ['DROP'], ['DROP'], ['EAST'], ['HARVEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['SELL', 'WHEAT', 19]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['DROP'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['PASS'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 7], ['SELL', 'WHEAT', 7], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['EAST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'TOMATO', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 8]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['DROP'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['PICKUP', 'FERTILIZER', 1], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['EAST'], ['FEED'], ['WATER'], ['DIG'], ['SOUTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['CARE'], ['HARVEST'], ['PLANT', 'CARROT'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'CARROT'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['FEED'], ['WATER'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['PLANT', 'CARROT'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['CARE'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['EAST'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['EAST'], ['CARE'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'CARROT'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 12], ['SELL', 'TOMATO', 4], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST'], ['DIG'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['FEED'], ['PLANT', 'CARROT'], ['HARVEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FEED'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['CARE'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['CARE'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST'], ['EAST'], ['FEED'], ['NORTH'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 22], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['DROP'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['CARE'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'WHEAT', 9], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['DROP'], ['WATER']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['DROP'], ['WATER'], ['WEST'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'WOOL', 8], ['SELL', 'WHEAT', 9], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['FERTILIZE'], ['PASS'], ['WATER']], 'market': [['SELL', 'WOOL', 5], ['SELL', 'WHEAT', 11]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST']], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 10]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['DROP'], ['FEED'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['DROP'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['EAST'], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'TOMATO', 5]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['HARVEST'], ['EAST'], ['EAST']], 'market': [['SELL', 'TOMATO', 5]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 22]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['EAST'], ['NORTH'], ['NORTH'], ['DIG'], ['SOUTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['DROP'], ['PLANT', 'CARROT'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WATER'], ['CARE'], ['HARVEST']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['SOUTH'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'TOMATO', 4], ['SELL', 'WOOL', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['DROP'], ['NORTH'], ['NORTH'], ['DROP'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'EGG', 4]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['DIG'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'MILK', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 4], ['SELL', 'WHEAT', 5], ['SELL', 'FERTILIZER', 7]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['PASS'], ['WATER'], ['PASS'], ['NORTH'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'WHEAT', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'FERTILIZER', 2], ['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['DROP'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['DROP'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 10], ['SELL', 'WHEAT', 15], ['SELL', 'TOMATO', 5]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['DROP'], ['WATER'], ['SOUTH'], ['NORTH'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 1], ['NORTH'], ['EAST'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['DROP'], ['WEST'], ['WATER'], ['EAST'], ['EAST'], ['WEST'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['EAST'], ['FEED'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 21]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WEST'], ['WEST'], ['HARVEST'], ['EAST'], ['CARE'], ['WEST'], ['EAST'], ['WATER'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['DROP'], ['WEST'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['WEST'], ['WEST'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 12], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['DROP'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 8], ['SELL', 'EGG', 4], ['SELL', 'CARROT', 3], ['SELL', 'FERTILIZER', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['WEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 5], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WOOL', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['WEST'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['DROP'], ['HARVEST'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 34], ['SELL', 'TOMATO', 8], ['SELL', 'CARROT', 5]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 8], ['SELL', 'WOOL', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['DROP'], ['EAST'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['DROP'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['NORTH'], ['DROP'], ['HARVEST'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['DROP'], ['EAST']], 'market': [['SELL', 'EGG', 7], ['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'TOMATO', 4], ['SELL', 'WHEAT', 12], ['SELL', 'WOOL', 1]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['DROP'], ['EAST'], ['EAST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 9], ['SELL', 'CARROT', 6], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['DROP'], ['SOUTH'], ['NORTH'], ['DROP'], ['DROP'], ['WEST'], ['DROP'], ['SOUTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'TOMATO', 8], ['SELL', 'WHEAT', 14], ['SELL', 'CARROT', 6], ['SELL', 'EGG', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['DROP'], ['EAST'], ['NORTH'], ['PASS'], ['WEST'], ['PASS'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 23], ['SELL', 'EGG', 5], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['DROP'], ['PASS'], ['PASS'], ['DROP'], ['PASS']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['WEST'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 19], ['SELL', 'CARROT', 14], ['SELL', 'WHEAT', 14], ['SELL', 'EGG', 2], ['SELL', 'FERTILIZER', 2]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
