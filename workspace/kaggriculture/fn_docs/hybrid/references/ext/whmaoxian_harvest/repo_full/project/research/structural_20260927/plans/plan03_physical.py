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

# Standalone observation-guarded reconstruction of a public production plan.
import base64,json,zlib
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rk<U5{H=a{MpzJP#{!G}7ixD{*aMWsfnELTn7dFpv!b1e*sZZ$bWhw3;D#dAqu*y3gTQ-p!L~4t4MOKHb&T)j$5v)xZ7x%U}QU%hf;qc=f}p_wTPhU0?nC&;R+a|MmHc&maH#^DqDLm;e6!`Nyk2eEjoIufBi#-K%$3*H^Fa_E*=>K3zY2{lop;n~$$QeExp_?e5j*|2{wb<@gWYf4kfLu=pp1KYaS%>$6tAef_78KP=jiwD<k)-MdqZzC8cixA(g%@geEv!{1j;`NPMz@810MdDuRD{PM4lEm^d3*+2f}>1EdMcyHH(_U_f|9U8MAufD&#|M2aXuA@);-TM#AujClR^^i~E;}5oHO*+1G{r2lP=1I%EX1sp2p11h;!_Y0~;?x}S*Vv%<yWN}5zx{6a?(X}m>y1BLkK?dhU*Nruy+Pym@Ikj|_1-`J?aycLjqivf2FLLG56AbMwPW?h-K%v^-`{-<t8%@Z@p$ZCec0WTUT33ycn{nptF9C_i}B_--lrLS=*;phu_=dd9-d#H@55N1FSNA3tJj^kvN`y1sh^%n-)AoM<AEdJyO`IRWAD#>d`Eb_J@V%#^+q3rr{|$@Sg-kVZ`Za4?_0bEMn{{xpUid`?g{UG{Kno_v&Q@QUiP-r;XCiW<aMVuC5@Xg&+Ki74`6!bgHL0HKCRwSdNOIK|Jc`e@80cRfB5N-yZaAs-@W~pFN2WS&Y69jSe1)M`o<+`Dm#nmbB^cSszr&N6)pijMvDUh{t#^vY2GAHVjFMu%s2OUKV&QM@o&ek*s@!h<eTJ?M+@-bgB<?c%-vX5AX;J2fpD!{$KC^nGMcD?wP#$xU`7_h|FD$Goh2sbsju<ba)&-XchSIywO4w`u_?!=#ba%Boa0-MEnb|~Vd&Y;S=ni5RQz-La6duQ$bU*cwuPH0@7Tgv8R=Q$9`moq|9{BE41^}QHs6XEwk#Odl-$j};ZZa%0FrS0P%sE=BP09z`~>&FzhFx-v*fXbV|JZ!vYT(z)_#2SacqtsEG)vmi~xvdx%klbS|i%V$sA$nQ`4sO6l^%JtGe+Jx@k0;B7w)peEaJDpF0ibPX|8u>95CEruN_a5BIP3f7spM|Jj@GWhahz#^TTkAl%{w%~pW^1LzpEWi{AElOtlshgTdIc)=1rjT=07j?X??f?;9}18h0g;yuTMZaJaCS4gqgIC|h5jW(|CSiGW+Pf0CH{NVZM7x|O!7(meBCRzbazY$#M{K|hZWcEe-;2+q`JAL(pcHZ&r%+7mitL|CLszbJfX(JggjJ6(MGT8;K?>}$@fqM@gg9GLt0>Fs*hYS*ZGIBHR{H8iP7$0tiCR_~sr{%>MG0ax0*D$MbRaGq`WEn=|B90Y@%bLbwG}9uwv|cW~k$~n^G~vLQoTfr9AZ2Eu_+xwxf+`2b7&c1uR9^PLJUKlOx&X&%l+T7!6+)=1?!+Z*qmt=t0hjM&Z=H8=4q91jK8bvX$NHn+40L`y=HU!@5Ny<()K(%$Sn!2wQho)-B^!*VGBZbmn;g?4Ai+$-6HsF8;IP*YU<?58kpadXm}C{^CEdz_s(JWiGyw=}_ViV5J9}=V6N*FbedQ&bZAf9AHS}yyU^g|gBZ@$ST>yVq=4UhwrMUEu<8o>sA@&T6RJ4Onb^sZYWrGqV_X6V-t>)v_rr_H&ycZgX^uCJFqCw0O=HYS!Mbg5`;A$F*$8{G+*kXkFV+suVtP5Q_ni$WF;&45S{XneO#%v*qbN+%9U}qL{B=Xoet+m2`3xWF6J-IpuZ!SXyRLs1K+1pvJ#nVE$F*PFG9Fwr!cx1NY^*jj(y!*7>5&KUO^ajX=*&lKjYm$LM&eZjdQXhZkpvnR1nn@d<jCQepG?=vj?W6#0@6e8<#LGK)@#SD5I`jpT*eX&E3X^htN{rRW=aNaO<|_KJ)OFyYNb0Z>JR-?wQj=Q*8usM)yozsYwYftjbz<SD$-h>RJ?ume8fl=XzB$M7`qY5iW;okUqH#5|{47pq;;G^q&}nO*ot-xZRpA6I6ikC<hsupR81i>_pZ{}vfC6B18DI!}>tkOip1MXnoz^9C0no4Q{;g=P1CS6L%W+6hP-%6el>wZLtpxVM$pkLB1xe5itcItX=(1B8LAIO<h+*I<gO+jVv|Z2roCwRUBiDF(XfOgb)>x5iWddgcqw%K?$CD$6#~QL<;=aqK<hUHaxx0J6n|ZoKgEZ!WA7*>`a%p3;MZPd!{H1xJ*#>t@Ix*K^DZtoFdbW0U8(EKF7bPPKGAPrH_m!=`Qzt=Y0$iN%OS$O!F+OWlD(miH^Sr)$>@MsNSOoBQXwY)?l4_52ufmRjosj2dXQJmxcCb~+<s^7Wv3NC$c1vg%v=4n+EkE8>(bj6PNAat|idpd7!2+WW)x1bxguBsDt;UtzGbgBq(mtF;ksh&RWWzXO#ghDI!^%OF*ca!XX^nWanxQ}&PlO09S}lY|STTC=g-~2Fd5z#>BXSoExIrig8d0}I$*=6MrBRxV0Vnl{b6(R+vLe(!^dO%B)q>~MyGo_<0#C9i@<&4$OtuZYTF!F8W9QTbu~zk50^&yQj9&m9K-(q8U>EW%c;t9XOR_D`OB6B?w*uJ`={&^1-Dqp0e@L-dH~~y31pb?u9f%eRuzn;Nq03D~N#HU36nUxoWla1qd~kVoecne@#EV#?I(3m%E3;9kt6R*GbW)ta`#3feleJc{gxVyhqJlUWySma!;bRKtgENcHZ`;m;Az^=Y(OAH60GavZg?OG72G66_(WM*hSY%SC;rJ3yi*W{NCelbKnhFd8pt6;nS@e+Xeu22NJf5FlJQ^N7M9wx7yhbM%nj`n$y?ytmN6!p4xakpy%&2(C(-@)ejop5_fN>5bSXy2L9fg8w;!VMNH=|rRis*-)H<U2IOk&1hHv)YlL%nP<Yks`v5idB1T7k9hyHPASzSy~52Y>|@X`WIjG!pF4HNgj*ffSu+M$D@KuG1MJ3P@YPUlcMAPPoa};hu*GL0%ON#tf-F6nh@`k>0-NRR921pNi;Qr_%np;PU{fMqQVH?8&ivF4cujnR(?1sDnx5IT){RWANAq#y^6uEO-NGJt``o|BW8`?g^oA07u)N2OCO9UwNO)dk?|@V8sE{R~%$Bw=TN@$rJ!>>oX~gK?(XQh-TDw5ZxFkSK#dcJ6(wyv3aU`<tA)xSZ*0H*+X-@XDuEALmIcIdz6x{>q08s^WV8FpK_G|2;|r>0A5)~OXE+To!8UDwE!HhpOaq%6B3`k`m6{G3fhVS1%_0L2w?DN{&N!Nuccj}taaM20U#hx7%uTTNa{V##DGAa;@bx&fw1InOpz01<^a}yDp*@e3662K3B57ky-3toU<dD}P5fVkSc)}FEa?q$(}4*)_8H7?TI^7rB~P#%Bcq#7ML^TRw8v-WLQ6B*H6W}LTN%BJNLKawt4@DMuuyC+;D|wc(M_b+fC1Z76$kWHT17Hqq6{$LKJCoa!z(Aneh3s13GS14c%nYvE7!I+v^H4=65@KTbA15Q^b$x02gD+gga)I#v|P%q00YVR4u(?FjP?<Sam9d+Lb|nx596o|*9s;4_0t0M&2ThD`dk?dH#A*#rPbU#8+_$S8nI*$1#|W1Wv5Uqic*9auGpZdK)8{^s$h2l^rWNAV8K}y^5Rm4;Jv%8WJ9}PH2Rc3q?XhWlg2$Hg_ead2s>2@&F?P`ov_OUdfEP$C_TN3m2lAH*`^{jNla0G)4|>`8cSPnn}y!J;mp{)U48Ky9R~!EVq?LN*!n3k`-EJFIK27q*6nUWTw>%3lo3Yzj6J}#mxpxn+rk#(xeqbT4=iPLj0y;o*U>PWuB;(2v}(HO{*2cQE3nW~gaJ-Cur1W;JN^?w3SY08XUmwzaUE%uF|^ff=2SF0p~$kr>`8`7))PipW5+fy!%{;_tn;>QZ>TcK6(28_c#T@}hS>nK^2DM^U=!qb%T@p!!#>ygkuC>_@_0qzLaXdqH=-&pd*TZgax~qVnLUUE0w2c~*l3bV44S@l%G!_EK_+c?qr|;Mgl~F`qAe$dFwXLdQC;c&#mmIPU}S5!XtY9fo+4=a&i)ymbJwe`3pj8I?Jc{et$$2-+uKQr7Rmgd|DVCxk}zazopP9qesVdd^{UD`D6_pdh(St?NR+}1oZV=Fbi$D)OZTSJJu9ka=hjFjDH)7rBC?mQiDT}0R`hsv!)BGF_(640jyW}c+W=E~z^#{&Z==mg$z*pOxMP;f0-w!jNi2R_HfaETmXub<l`C^`>ORzj&}|jYODrq~*{Fp<=Ds<+6r7FACEZ5YkTYw~8ZD1lADZS}3JK9l^vR+(LA?^^A-0UJYld9_#fP!1j;hR{bdfMl415jdov#mo8Ez_(yF?Jhskkvhtj~`WxaTdT=6Yt()(Eg{45i;QO}v?|>~(kQc#bf~D=o#2WY_nypDalj7IUI#$>4tf+`9X_4;Bim3>A_Ugw0FtV;7Q%H~q3i7Kenydg$J_buBv^o$@pkpj+G9U<1tss(iO!#T8Lii|~;C_O7b|*?Kk93N!aRhid2)M1BUgta&GM(q29Pr6yccDCgI#4qng4dG_qrNyw2297EKS9{O^-h+!Uf*ESd7YzqFykeNq8!AQB5HlW!!YCi(mRfwAfC<k7-GAT#mRx~Z5#7$7wk00yz*oE|YrAPq5x3Ieo%r%a{7f~kP=ZfJGRt?!${*7Xh$x8R!FNNem=LK5%N|f44=z4g`%YhQ}Rj#VXV?H;Q{QRave}<};fU7<pwcJRh1gl1NOrB(O?RsB`F6<nRhpWvGBQ#4DF*psLG6;2Umbf>Q%^5MDq(<;;!=`|QpJl;eY(ZY+_CY&zAQ&j99C^-<KpiajKV8k21Pvy>nB1&T1v5fzGejg<k;`OFCu>g7WYg5O`Q<v|Ad{7?v(Yj`d0MX0u4>L^*bC-CpgmUH#e3>_@z=6)9rT#x0g2r=-vE<kIWj68%scD>v67smwTmYXh@SuitXx5SDhwltoDqQL5m`;$G=O2i-+2`Wj~=xiUuu8VU=%pYVs*-3*-Z&zu{BQ;n|JfnG#LL&iny>Us03c|sc?)KA}NOA@GhyCkdTV5lo9g+#C6gsu`-7e$NVT16CLVE=~{zOi0FhGa0>AhFJiJnSjs))@#aAtcmey``o)?vs)Cs*wbStZX`zMv&gc%Kc4C5&@KO^yhE;8LU5Z^Di2zqCJ3Q_9kILDa03ed19dm%RWj!;>W=n|1@#Z$Iff0_YTExv?k%FL1ZMV&rp>nGu9rEfpJ3Bq`O7|0oW<a7+G|{0WE{}a{JwULB2YHPFcDd*BP^C%9nL`_)r^Q%O$SGbP^#h-m?bPZFCgpFIhzX6mYgkK^amY7Q!L<d8fHA5FVzk^--dQ{WECOvUB%CEw?Mi_dx`{X;koo!??`Xm*rh+LWgphJJ=L>D~saf9Ua78_RVVfR#g2#<bYz*}tU>+~i-tc-Wk-{pXN!oSO6#;KbkuzYd@+vX#a7^`w{M5aYb2rR#IL%DyNl9IwT(vV9brik{ZM3)#l)BfeTB<QliMLdV5t+Y}5-q23A!N3eS9nJe4fGoCL0GWz8k9t4o;S<XDWO0SQHvj#O~d_Lvd{eDq##d^P#0WDf>9N|HZz})*R6aDn)SAy8nb3@WMVv)wItSFaFr6k7AMm-NnBTvNmC&IP)$z9AsqpzJqi%)wIj3%mf;j_7?T8{cDpG`F)b0Knrwt6)=7s`2IU;2Ma8OUItuV=VN|-U0mHf5%%_fv)w2RdQgcxqR4Z?$mM4o`D4Byo@eNN4H){o5=8-W-GySkp2v;u8ERiM{B;+BgfkQ0#U4;x0i2@3_WYhv8koIM=Z-xm4%Q)EWuOS55Ckkx!FPG54O=6pe-$Vh9^PiAhfoBWYLNP76wakbj8a$uXN#xN3MkP4*gy`5w51SV*?*SMzIjA6`Rj8cKY(H8^WX?z{;@EP%Z^u_RjGE92@n!9|xv3{wWen-nI#kW(-a~dC;l1XLQ%ew=$=Ao&wWmTB4X(V=oGf~N?X^)(S70b_W+~&<%z;fPFXIJpUFB1M#zao{TsZ}<EyrW@e4cX3R7EO^D^1JP2!Y#}xu0^o+<dB1lNd5i_q%Z<T?`^43@6-FT1!s5T=1$WEf(Sx6CwzfsZh>fJB=pAT9Q?y`0s^$r|dG$db@@o2K5GvK$f}~XgY#-OOKEt045_C|M2|czC8`~%M4Xk(ASg7fPfPU?qEpGP}C-+snBUHY(*G%V#Fl2C@3q|E<>4W>(ab9*jT5SjI@EAlDJ^u13YGNI2`_%ohr!>Y9P;f{hRCA;LlSrO<1(d$A36*4lDvPumSc01AbfRAqyBq`}w$2e3TfR2Yd({QUxY^H;-@M$f%%Y!?~FTcG{<#bkZT2rWFpGRX0eP9_Rr`7l8!>YsD$VctZ|!GuJ;YHIVh#+({*4f=v^xorDBOyfoas2VbP+EkKY8q2>S@Vk&&c{_vqM)OES7NF5Tmh|nmYWD4M&8LU62KN;{}$mny?B<;E|BIky4+b+od^JvwD;GVy8#+eHqJO?%wEyTmL`kPVocwKNl94+u=mq8Wh6*f3jjzeZ!t1yOH<2tYATBDa!ZCIsJEXr%4XkT=rl=$2rCoD}7O#Cu={ID`&E)E&v@*>+v=#fz4t}KVQk(GJ`fRyVfc?Ci2euF-qFELWbEVxm_D10d}1)zgMz%@@XpK%KNxMU+N$a}Nv)Yze^*qm4ZnjLLOKQ@=_2vW|$<l@B!TO?C<ARXZB7oYr^&L;?H=O>jWiM)qL**A7aLuZIo<g1iioK?iGrEQIN)X#4U*-RPKR|TAoyCFgeDmdlFb!~=F9ci+2!=n#aa2Of{BCi&CGid}`4WLdAMS!|>lsn{-=<7%KwUkhYjT0-Kx9DecCHs1DSUbxrjq}#DS94tzmh(p?@3;usF#n%aRjif9<5?&pWGUd#0OwH}l}VwiVn~)QXyA8peTjHb(q9STgYK}341NYy7$-)NAJwOWOi6W-Y4?^IWuutX^^6n}#vQD2qH@+urO*jY&Jm^P%%C|WoX`-;#YR7gsoO<5-M~z}Hm68+1MU~5FNmZy9aWQ3pYRPluT)5SjCorR3)|96A&5tGX8A2ieDvm$PB~qkYAB_;R8O4_%aW?8(owZVvQ;9_%L<`D(SMRS5G4hb(PiIGH3gGEW9Tl7)}=)ZIxN<$Mr^1a87(TY4*(6GGom3A(ubDIWm~C9@^$8YrR<e$?MtR9)I?;=P7Sy}X2up}akq2GJrxdM@pRZq6nk;*^z|`lU<z@(ON+$Lnd|216D!B)9b-!oX54@u4{;KnE`iOuW~r&xk_PJ+^1KvFUnXSR!_4eDMftF*T<D=@g_^1XBTs3HeWh5{WN4LhxE?Pw=313^Pq^#A5~$ZKs3JbV=)ky2Rx*i2ed&|xX+edG$z@1&@0CQ5k%3t{rvz=L$wJ5Z^y2claCm)sko>()Qal|<kna#{Ny*9BPh4`65lr(ENwGvqW`Rt?lma@9M-lzlw5Av|J;^tsX!d~EDn$hBtWu^bU|Ub|rXd&1O=0w@Mx<3V2JikiZ@;nm2+y_yMTnUQ9f2b4kq2(Q$uWA_7MNaK*N?+!%HsnsZm1wpTsZuE=Oux-^Ai0FGR_YR{dp<wMAC3X_3g#nQ}Hy`>v~;fTWJo74gukk;2FaWQ!}=Idr(f9Y_qA6ZImESSF`7Ev|oaR^Ld@W-kqn|xpbUS!5)Li@2bY~>9DCdtWfafivttoB;O`2(O2{gFm;s3sA07}RQ5VR3~b6%;#@OuOS)X(QmQED_-qeb)}-U2P|mJLEVgLT?uzEQjM*B=J-$vD*wOP9R)H(yE3$B$u<Issv)r<;Jaq*lTC_9^V=Sk=eG0u3<{%msn59NdSM#(cJSVGkS#-GO>0V-ZC$dpo-ZC*kIoZ%Y;EA|34aX-lzS2a<cK=hcx3X~-X&7}$@<zU2TaR3D@D6S;Nh{)t(Zf8nls2NAdO{D#r0O*-D!mEY7s<NZ%9jC8SDh}rAgR*e-<)Qd9|Y8E4&!VSdI}`~X=&}82vXvv(9%E!9YmQjm#?)FF-br4Fu$>B;V)@mp$H@br5p}#LdeIH+=BOv)qY%WSy^pdY72xn#wyqe+3Bj@&*nFW6!~1AjUk=CE75)qcqc}Go?le4`5Ya(mBmnPJVGmCJ=?a-XuqgU!Dbra0X21-B?km1N!0SHbmB~j9YjbVcEDWZfO`(}@cQ?o`Ang&RaUDeo%?)nkAMsyGySRnz}OO#jS9lt9HX46F7uE=gldP90heXUZu;6i<cK#N!ktsByH8AUs%{n3UaNM_dQN8~6Y3&BppGZ4!b3sxCn+bk-x+KIe<uorB0Q)<eBfn!U@hsCjl17v&dT~Iol_5q*o;<5A?E@<-%Y4cUVoVc2%%}Xa9s}`2JfFmgp(<RPed&U<~70|mIGjI3_a@wYx2>#WHN&JQVfsOUS{irI_z1Rq{HogvpzYw!BeCsG}pR?x#D4VQG!#86v)KByh#6aN&ifWhvAI_H05w8X;6%m0f>2bItbDc3I`|_98i@W5EXb}%9qzzTsQn54(9Ryxxozbz@T$l@il@$pSFTmLDZ(`1s4cXfe!Vzi{gj-yEh+SpSG{1<;tAp$fEPbAi%jeF+AHS0=Azes??EV1zg;`z|zW4?dayYME#AW_6sFc{J4=YI!45KDpYEQ22llAFaG)znjhG`^xz`tNch{7_zM&@%4}{f978s)$D+7lwI63OaCiiS*|=&)$@)W+=?PNgT34U5b*^S5btxK~Vvb~qXWo<uu)c)`W?Q{iu8#V1U;Km_Ff2T?7yv6F&7G?{b}8~*&ZXp(IUBrm=4e)LfNNzIZub|MrIb6dHW^bPptm|autmDF$%kum_$YG5VFjR{pn;XAqVW|%1l}P*c_GRwaI3L51j_M0(Xv_{R(Cf#6nKSHvMM!xE5ccs09e90J>WFVC1qg@$a3Xms=(=aX<31=+3~|#S15@_TuZ_$L(*=i!c#XFho=A%d;xR{*y4kT6i-gO9ZF7PIpB7Y4T;FKwR7C;G`4Yhr6M~4Og6UQ+1Ox`Uo=_Rv$FLr)0!5QFVrAz)K|h$Xo3x>R450F@gt~xXAJRo%B7&pq9ti*kF`(MUfl)x6(dEhlrBS@vW}oRSRqV?2^f%v$mrgo`%d5>!7E;nsB}SU^Awr@LUf6ieg%L*dPCO_Av6=Tal^XFL_n%1x?l;Z;bjy|sZi{&E{l5r01StrQ#~Dmu2nVd+YSqXl>;kr?U?=Gt7wd5#O8{%*(x#N4>dEFPaq_~DVi=OFJ)|Z%Bc-r@Ca-wSyoJR$pai^jlih_(=}ES&+?&p*g2e?QBGoG*#Ks-0%$$i)#BH~LT(ap%2H$utP}w+dQBWDnn82bl#Ufz9AVEoRRbs{w5$QOzq@+}R{0|*D%rNG&^)rtW&Md2xWoaWYgBR)fEMG-CR?icLeNnfPPVhvm};s~qk0Ap2}l#gl40OSc8$3v<3*wX+o{wuJEJWrQBl^wt~sVvjhEV3ciCe)f{=jljyMc8g*}aCCz0*u)9g$tuFRo)jfq)oQyCfnA!E$9r2KF0i(IUbk%N3kVqD3wa7i1JeJm%POINvJTZskpX87(Et$DEf`O-?&X42$9H$SJMH&68}JrYweGmGMQAY0>b!-Jp+6Fj$YSpycWgvddKby!4PSLMq?wv-DH0|po4EeRzpKx-qrgM`!PCZbu?Ofj%jLjyz6tQyyxEGNRjtgwm;>J`R{96}tEn7>yIig7o9H)-k#ltij6EjB4ur4_y$oVu<pjLN0#k{nk71&)X{lKskvv()@%IcJ&GHx2j`sg~Fljb1MND=bN7MF9@*M}hMtcV*6%f?GF1cC1QtkCX6wDLh1Vw2&Dcs7gX&zB=$+zO0He(WI}xi{!aY0)SkEtMo*vb3#nJAWGLMByEwBRKU88$~4`CX^C*eUd_%S!-~=p&&?`p9UY?7NvcOBgd<><SWCheePqc@e#>o~xXx)@N|S$GTezV2NXfo=MI335jVgVE>2Jt3X`Y|}-JB{*4)=~!=+VXZRIX|}j@+W+$znt;_;z8u0iM|fb-&wiu$1$&{o8VSM(GLz4k}YyF*LTVQjtnO#sWtpyjw`t^i*gC#6n3orNg(tL_-&y0DnESe)>sKr~Z`$@+~E!^$j}BsRnEbj};+gbJ>IwceKjv;8>72om81utHo}`FH4C>;hs5rx{4`uNkDwv7RfzI!jDug%TA!ko8hcIM{iu!T&u_`MYarG@@gHivf)w=iUEAGXx!E%{0NmRD4k?q6Y1$<(U_hC)t~J!lyo?P|88WMDv53uu_<Cl6RA$Mj5mDVAL~U9l9?u9NQQsU`1<+b^`tnFrN2^?vAh6KBut#0R|cYP-OQ8LX84sA+rLPLBw6S#gKDqk7ix{lgj&4XR~pr*<ropamf&rqm=B{1<c7~>yxLfyR^>U`i95mr9?0q{CF6AYgG$g><nK&L`GB>B6kMX^KrSbiLoO4UMM0B7=nNRAy17B9o}31EILVK>hQ)o4-CMZGRO+Q$COYNz@w;K}ilczHC}fw16x2zUx^tH#QRsC?6eagXFW(hp-RL8Ly1eRgp<p$!OvVdO(KDAO?s)Qej->%s!I27+SF*(mz!l^4ID3APgd9Q}swz@UMN6_&lDS7?Yt=tH&JNvXED_MIJ9aoakbC|+hqp_JKl>dM%m$!Pszz3jSuX=P3ykhJTr3Ti<wLm5c7*hE<V|f_{k7|*ZLRtcQ{-pP$EF|<YSv9_I^7qAMn)^E5%~)@-F(1Jvnr{T>A+CmMJ6m3rAq<vr>wW?(+-|M;unnjV-F8Q$Wl+n>y62qS6PN4Dy~3>S#{mO!jO1hDZ{|aTT5d;Rjv299{kuXAWBiZt%tD@8EO&EOuQv_p3G+{44&z%1Tz==a48xXXP7|1kdPHXehNi3Y+co^BU`xnN#aHZ^RUQJk4)02XqN?^gI}o@lbI#ZLp_)sK}mcpL25dJLwKaLOs31?0ZDomR9H&!Qabl=v7=23&*=3<Shw>9Yk~3%9r=Gc@GEP&2APBg8T(P0l3+=IB~RAjSSoPVS`f?<MZ5sY70bSj<#|y~iV)0Gn(UyT*48|uS5UB|rl$=X32>i?38lX-F7_U_bMw_;J5o`|WaQ+iG8u;F7XWeqY(vmvd{h?lw(0^x1i=xSK`0=-8&t;L`;pxOQ#_Zo^;vcWf=jz*0}-y}ZaDT1rGq?B@={evum!Rh-h^EZS@cPoHyihuClR0hNS=o-<=3&{Q34gy_%TIh2Fu&?^d}s-_xRAJMoG7zeQoaSC_a<FW1FE@eBD=1V#~qe8l;mrT=>3FYs^RqZ4|`Q3%?barK_7BFy&?6=i!h<JQSn#@?9ZEK`oOcbRanV#Uq3gU3>Z>^vD(bvv_)%$6xKbkl=lE8EHC{RR;WEW4|aMXX>nx4ulf5bgd)ot+Vn9$e@R_FCc_ng#&PMbqk)lM=>^27FVR*+8Tv+A5S~a;8O<LkVTrfO}UaaN;0E3QQX-=$HSQK7fCwOv$Ew&ifx?)^_&#l6S9%X4K+A9`iA&bDJ{YK&jhS(N(*Pn%^|dG1rAcQ-j37UNhB~R*@JS)b`@R>&M<Snrcjn_Ma2^as0PsSs`6&K(W6dyUdk$1@r&`8d`vHK+=euykuT>dV38lUR&bZ2L)0jn39dQ@#o5~FaorRF3A-S;oy!MpkhmBo=_J{@QHjUpCTU%SiI%zQ)ca!5pQ@%jroA;Q4(VbggVA{PGI@4p#_|C6t7T1g%)O>1h3z~q57<TG4WiUJ#?td4&HcNgsD#=fmHbu$C-oZVNtx)e1ED%2(7CO~WresVl|*E4xT<YzY;C^IXvPb*@amzz=);0{qOvVS02egTn_v}*M-}e^RUt}tz(%rWJG2MrAZ=w~>nO&;h*AtZ7)e|A(4tJuL`~D9m(QU)!A}8y&OX$%5FKdXFrS-Wqb|21?s&O!U0*+o7_>0NxDRRTT?<d0X$8r(Qb9?RnNf0(xIkK$LeUM~3W^_-LBm5vTzR~0zm$G6ZYf(_qB=+nXD9@^{k*JF>zbLYPA-NrH~0)zx1h>zFh&Kmk=<*{lkK);25}qK<#UK;QdcH6lSVd~`2Y<kZunHaEUAj>bFet1SlbND-~u*v1!-XuTa>x;9c)10MFW?D)J-c;E=?xHNAm<EtmzaKeW5LH&njWvI6gtkGCq4L?Pjm|oR9v}Zn>%xw~i6$g}h~h!R`Z#yBEBA;Vxu43$!{)42l*h$Q9SCxEawBSgqb=571FkaJ!H%uU0=fKo%6(JQ8j4qAOy%Tmb@0oXqP+$KTCX`E#;zKK&m|y%Ea')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
