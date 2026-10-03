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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rM%%Z^;has3yrxsc)6$UBNt(h#DC1c&2-JQxT9EW>~yFJ$iw|GTN_?pswiPn<Xr8JRaPy=(NNx+-sGWIWE}r~i5NZ-4&VU;pyASO4_WtM5O2`uyFipI^WF_doyVzy8;k?|k|4uYdmAfBfaYzkL1EtKa<i$3MOK{@owmynprj)!Pr(SFiu!=hsi){^4@@_RBZ_aC!gXd;i<uMZSCY>GBGH@$eTve0RBg-2V;!ji3MbHT`fuz54j>?eBm5xO-Lp&D%TPf2&=qkDoq#`{UcsUw-BK-Q~^ay9GGsPxg;(x4_rS51${`_cuSjd;jg9KEC<k^N-I@YFo7D*Z$`3-+Xy8FE8=9l0RJDzrTAkzapCmZ8`T%etiGt?Pd44pMUG_i|6;)KIG^B_x$$$arZX1Z|~m5mw)>G=ZBMlw&m@U{r2xK_wa_;_S=8vH=i$`9zXPL$!}k^PYZl#|4@O44p#W(d$*6+KKsa;ZR^sm)b0(D|8RL@ZI0X9{Nclo&+FB`pY5l@r??$1_*lOE^x@;v$9R5t^mEv!1fS;EZ<oA|zbEfj7Db8M&VPI+YTO;ULiu$72MBC}cGDOUspf6>#Wc9Hx2N~^&2v<^ZS1FG7Yktfz>L0%p7dskxA%&EsD~B4FxxWRU4z^A$X<^G`E9kHKerHVUrwX5ME9q%`C(@?<V)jz0=8?=OS{_;EXgfq-CpPRJ^w8>*$8`P?i-}RWdF9L=hL2(?cJb*=f1<YAKt&ey#4&A-(Eg_e)s;}zdSym$5=*6f~POqz4XgjxqI!`zy9^F-RDK)#ug;+Up0SW+CPCG31q8E0{z-pXeBbTEeZb5?u+!Jm*0BNXKQ!!{wNp+*?(#I(}82C2j%tyZ0YWnD}eMNzORkKeaY%H5e9A-J3mf15q-Kl`d3r@wjboT4YchBRGTy#J9d+7uMILdR>242%dO~Xs<}|M>#QIxBtfMO*7CLni7aIM<J-aCR`M1e{D%bc5i2g!y^+e3?^k2{9JhDB-z1?Ou}|{w)#EP^cx5B0dfg^Aeyhj7UE0rK*Dax^uur*ojVS#Sw41>D2WLL>AntDSmz{EVGwzQ=a`({WH<Jp1jgCr__)GU?zFzVH4o^|UHd3*`B75)M_zxi6A<g6VTE=6Bf!#9qNTV&~EiZ3RAK&F`Kc$=8gZh%x7>hMIyA~^3zk=9CSIj&UJqz~mYF&TWybC`y1<i7EG0CkQ$mrobGO#I<v&rw?eER1$g5Q6a^~V<5{xv;vb82OL#j3ZXrzfG=z`Ngh`N#d%SUYG=nlRCriO*Ks(LCS9a{FX-OpEewP@%4~BHE|NgN$Y%ef#wH8v%c}e+gDzu;)ers+zZp_O>pdB#JE0b4~rj=TC30zqx$+^vAXlX4Tuzg`+y4YC0=M&HVHk4}ZA+T>$c!wwb~6f#W}y)Wd3<+-%0ywb=q)*Y<sGt&F=4vfYRcmE13{)4X?H2Si#DU|f3JJlj`oe{}!fdIvCVdo(hLF&4_Hp;&(|HE3>cP_xmPn(X=;-fbcUyCC^E)vT>EbqOqevU}uqA^PX2(n63ghIP)&*-Fo+1z{ZAMa_rof}^zmpp8wD$UzcC&_!rxRSiJR?mc8W4UaI_>Kfts<8TzJ8S<?&ZIqwNu#{cW@Mq=ixb_3_`GwYra6>&wziIWakHy-=nYT=CUu_5M>5JUx?Y3ud<7!*br!R8p1ZXHf{I{MVA}y57L~Wl!h3AW8Nx`Q@-5_^C+noW?+)d3y=VF;92Jmn&B2TS#<ncCjuePdVkO?RoM@4NQg^&izu)^poEQIz!3`og9F?=4(+7_AW1$>UW!Ekq;@8J)1Aff}3Lbu0Z!(xUaDF<YboZc-vQe}laB<{q_dyDVSA@2`GWvL<kXBa9I9Sf4(`&+$Dm+xQZn_$#yllHc_17RF>(Z<##hu}c>^^2G|act;*?dD^}1Cg2Zo^EJB5#pM<aD{BtsuBbLk07>jVx&`dXctET8-O>tJDRB-WT7SkCAEP*0jGuKXsj{p=H6g+@xYB;VLM!M5-%I-ueVU>6r#F4l{;85Ylio-idaq*KsQUpF-<(WdVs7Wg)aO+ABL_X{U;#exJLmX<=&7klKqKtPt6}rq?s{;E1LY|VzpXl9RxrEPt0dKnehgzu_z_2zs%H&tndT(-e_63)0(kp9pcV9+vb`EJA<^?lelljTQ%yhP_YHlAu&P|jLBNnR-mQ=&xIu$w}yEWFuKbCj)~mA(b&HOtzhu!+O&;yiAPh5$L$A(TgLI9lnW$(IW@el55+2Fp`={c_Nz5@qVG61qMZbM+qMp#AA-vVZc4Xa+|RyHa?U!O#_w?Ol2wG$5g#KOCMICJF|Qk2_oYgb4hx9IK8`9kgQgfT`(E#!a*3_6RAK}k7I+5|UN`X2=!XP1V;`-VeV`QR#{t%ndNW(OCU7hYo*%Z$q^Z<EA*mGp*Gt`5v7>3ZTt9qxuia1Y-+ce=tC@Kh>_`xB7Mx9VDyYZ=nB6jFkz1Lcl|#tj!V|p}w)gabuPi$7ATsElHps>-UuJu6M-xPGKw)EJ&>Ro1J$r8A<BBxx>QdzqN%!ME31r?B@I~8$4rI%}g@#PX<`DG6_vBxZEx)8$Ppj`0{CyuOPl<tPl6Y$A>-I!~ntN+#`0U9?zKcdis9ji{{XZ0Q-J>L7w>rRWz}SD*%(novUcp3*2uL{8Cn0XY%+maAj@rBjNXU{?px6XQ3v?9ev)&)YGA@hR-IqY&bvv!HE!l%owl|jbgGQLF`3-Qe*)H3qk-aVVx>PMKT!0#4pj$@ToQ7ml81^^nLu=DsGSuX~UUO?%NlRGkExzx)jjQ)xb8JMgr)YDRw7T66Vvdzd@QYxOgor7ANC=2V+fUN{4FKk`yWK%#0+r+3zDFr6V%uyj>HHuNoNM<*l(UXrhyLI0qX7}Q2?>q1sPBTdLE!a5uA^SC%_z7W=lirBX9}}WzY6QDm4H<sftQvNE`39V{N+HH?E$0bu?P6cQ7i{911s&kK5xWcL|GMtFJSjaW~fTfn51av^Nx&HIXf_Ew8WA(O>lt0u>C}VZ!7D8Q7j5*)@a=1wN=qtYCOjl0xAdILJW>rI8<0@DXFd{2Q?uP01exvNi49|3l+p5orzR+&LOOz<^$awvY*0}lJ40{TmiT~Bh-Ytz`k>K8=;_8eb{-66yA*O82}qK;-9%r;hf%9R3ya)PSPlIp1YDcVc5BV(QMc))_GQe`p;cL7~TW>b4TwS7M2+s_#BGg<2O?aN8iQksmkE`<EC+fsfK#}hh_A;1CAhU+RYl=i}YTnabwt(!f@iOTl+Oxj7VH;#Vn_=)vOs#dY*jkgHKq^uUlBdm4iHh3<}xd4un_IjcoV-&;}}+?M~7jZ!g96!%aqn9ABVlW>e^UFHhkQ@816&$XpS*Dft?Hdg+V<QK?^1g)35kF%B-MR#oPH>ux_qtz=Rf-7ha;w3PKF1~!TcIYcdCmddx>z9s2@fi1m%470`_puJ+~3BW6cP+;M$K(ltBC`~*cUyEGwx+~mRtNP9EJru!IEWnu*=MJxt>MlJC4eaRwc@>&&1?}V9Cl$)UdL=jXGXp%7rDFn``)JK|)yZv#b@C&P2T}6v_Bi;P9)xqWP{8CF+3kT*rmZV@2=OHswr1V!fl3cu1VmXM5B(y6uGtep=|68Fb;euArO~cJz;~Bb3+Vp1$*Q8j)y^}`$59mf=Np^W-B1yyLkfq-<0&GY%$o3xtKKXmL*+_msHTymj9kSY;*DisEtjCZ?z$hx%=TC}_>;vpDh}M91I+^ieXn<n8F5D(5SjwaJf3fX-Hbdq;V{&eTJ6@dD#^8?2gyx}Ts?mlB+&d5lo%<h%s>WqRTv6oICgr8fIlp4;VVnF^$2j*=%z>Kt;n+#>deb2YpUv_AibN|rbW3#P9j2)aO3wA%_*+F$X*V*Tv`{;SNzD1sV%JyzzAe5wwU5ddms11&C}HKf#D{n-T^{6*IA@wOK?SJqR#Yuyb90IKb9o?P2Mz$TG5TiDIZcOrTl{@BR^anL(weCWo6<Xh}uFN879|aK(RrpqcS0C^Aj3v=Op6XD=#WM0;glfy8_jDjV$IU6%dEAdr<)N9#bzRbXMFu8>(Ga&-bH%D<(+OVvbWP<fHPDA+$gyR;7uC&POs&I_;%uZ(0b{@IRwl;|meqT#P^>q~2f+fgqZ$9n-t*P!3&2UO|ee)luRg(bH~iTBkN=7Ibas^{=VvXM6@?mD*iu+%-D584_*N?Zs)YtM`L*+njg9@51!+|AOgBZBu0J@Ihw~&KeSRi^m0y_7Vm~l!@8KMNrFUN|xBqXAvc_5|l|j(#K6ASn)=LCyh{1jk!L7BbP8x03)6@i$+_YhLed1)5Bs34byFL&3Q`^P4(`X{D>w{7y7K2OUuXZAims3Z|hFXscJ4a`Eug{6Pk&LsncA$c|vtp<1#^9NHN;|Wr_4LVIKi`ywV_{uEx+#KAX&PcyJ<P7+8EH@ikPE-R|xZ@qq#R?TBMtXQ=`m4dL0Q=U6%JCj()eQp6$ULFfuC%j3A!9Dw`RQRj2AmYx1oj?kf;@L&AM4%INic1__)Gt8s)L$FSuA2)1;fFaP<a8C%9J_(}F`W*twQo2KY>4<n2FV001<cD+M=#Y@gy;pf*{ER)W40c0hvHB1_g~yZ%0ECRQBdX{eC38_(O!-znP?mx=@a~t7QfQe^_ZfEitb4}A&r#lkGNts8bhh0ben8J=X*4@67Ux+*#t>CxRzRX2ek}&5r4v3}5Y3~Pj?QF)`CtGq=SMMP4HrbUt@+c|eqMC5)sa6IV_Ic}v~G6@_qfYNimWQd7m<Ql(u|4HG?~Och$o!2LlDH%WrEWbsmh3fCd%#g*JdSK5<{d^RO`m>Yjf@DDiy53hUP0xr^_@MntKAOav8_T!#AAt+h}C_w_gOCJyUwqi-KClge~U3uIhF0S^<cQ#gd&-p}sT*wOKazNMQzYB7K=%0A-<M4Ig`&>TtCQE;7OLM?VOefTRJ2EtBjKm_s-|-|>jRMR^%(VnBR2n!KIRt>Ilu<ZvF&U)Co&Oq0DLl@yORnj<Ie;V-t|CyWuv?j=_6Jjkmt%`U*E+_7l|<r(maaF2|GM$sUh{^>xS(d8UeSAeFdZj%?y$+ZHhQu7?Qk6rty^UF$FJd8Z%<_&b69kqC0>1e*dYaK1ETXq@je`e<>Ij`Ac&0}f*leGsacMs|(=v5lfdxWSZ@()j&CA+(u=dushLx^}rr7hg*4m_Di!FMd2E`)j(6Hq#=L0<(#9J-<9GxALcT4S>;8c4yfwGNNw$b1~|d4yiz1njgED?Q<h+usO|X28Tlj?ZWsHkd?FA(uRDX34bCw==Lk0NVDr85IOPCKw4W`XtL|#I*n)9M3`m5c&W?zYNYv?HC5dg))jdMjc(u;HfYhqv5I&N+;^e8~pTP<lq6IL-`EROY-?dKS?QIY1?gyYFbjss>*+0)papkG#Jyi1BBTEY#iJkm3G}9e;)`hoX_n&(S$`CpUw2Cl88g}e~gT)6%eI8jljSk41Dm0r$+4Hhm27bXpjzz>3*Vh7bIm8j23it$f9lI@$hQW6x$r@kBq;E8P|YKPu<|f$A#sJmXIEqa1eS{pL4-3(E|i}*W~=viog%I9qMf2wagfIgTkJ&h_Jp>P{aySiSR_Az@24uNA^f#O1m5?3rW;b$Dt?K+Mj^9=)AH6YYwC~4EBX1Y$RT@lr4WerGjxrS;%caJ*8wNWQk%Yw<5gy?L*KZVH8`Ad9wDMiK6Pp2$1fG#tTjK{8oT=w09eqcp?LBXlE;WRCu~0?0cr=LPcen79C-^m~r(4t3<9oyCO8RwgE!X0p8e2D_)GDwgJ*HE5ZW6ykKK$7T9pyKtXq!R)pK+c008k+iI|i#Z2gc4qdM*f+UE>a9{ue0E&)8%WnQ*A0z|<&q6qzMJrBc(^9@-CmO8X-x*vEK-kl61}>NdNfqZ(6<%S-%ypm9;oQJ_%dD0@^;og7WW|Q&JI|n@)*Anl;epX}xl0TqExC0X=(#SS`aKa`K<T*y^|bX6SJ%?!a4~B2E1;Jojzo#Db0}LJuU*a+%H<idS3rU8fYNu0JjF8;<4P&cu-LaQ04UvspJC|AhfkLn<isxTW0F~VR=|UxlYaAwP!Sw_SU_zdknu=sVyyI*5CW49n~vUTV0amzE3{C|ek1vHjzFqvGj|{4B(R2$7m7$lw~h^G?TY*2FN|>8JQ8O9gywpN#-=038Ee2*wUg>8BHSa^z%OzKDED3k4Ws^O5?2$+xwkRNProb$vu3~pNlb?4x=?_%y59>Hnm|M)KmeL8K74$4v6>|Zme<@`jso+8*rN*{cQanfq-Xucm@wRe?s+|i+#(Hct5-ls;E0sR!{=XnBj$JA*p!M2AIzBj0P-5bEoiY1P`C$r&krAVGD#UWtmLgN`x2O)>V}u34q7l)JHrt__eR%_y2ePz#r9FNp}%1DfFY`;8pBkyKts1w_TmIis$m`kb-E^#Y*5XyX?1{ea(HX|VAD|DOgMni$o>MZLwS!eQ#>rs+bWerft@hjPYLz3s9K<JzqdI1D3@D!Ln%(eW-WOJ-%;@*gSC(*>Uq~FecxRz_dSkKSN_H_)#=<I#MOCOm5e_MxM&5|4GyXV9Hu)COnZXNs$~}Yx|r;hb@n7paoQ3B0Ux8T-2HtnKyk-)(7346=*^}btu~y~)60u>ER(|&yCG4SY$Pqs8V=yOVp2-0qiC6-i$X76y7^mWlQyb1GD4UpEYt-j8EkiVPB|KlrI{C7<IL_LsyLb>k>R<G?c&ZZ;xvq=D3I}27CXi_8pi!N0&QxGPo7As!%7uHvl#thf^55c30vc2U7a}Y6@d;D9;$Zx<@L(2&!b($$X=qBs6<MB_-apoIV}J)<qN^r%YiG?J{=U>m75LqUF<oQaGj$G2ck)U;sOYb-uH?NNW>5*>FI{5iHs+Zq<hXrH7%mb=WH$HCmDf}kl7b)!tjxZ>XAG}b8P`dZPJR#JD954t38es6DEuY*>$=_tEUZbNH<yz*P7M4?1)!?J&i(mUKIh6q2Lw^r{PHqNSY!Wa^-#%zKQlg$ud0PG=HTG0k)W2BNGC8nHSLom9-DT)_DR<Xc9VQqCfUt(ZUE&^rFC#On+o~GV^LuwM7Gf{bOpeZH~9Ix6gI=VDK&QxR+}TP4iGn7(;N^P*M^<Uib>ah*Zus>DsvzQhEU{a`&6@>Qu$XrJ2?vZX-%-A{-`2OyI?fRc@>I&j3(LNmEr@Xm6WS5zxoR4o6)Bt39#3eeC9+Vi1Hrwj+!S&@F1YZVrnpRkII8NOal!h)&+zo|WNATXFA@bMXN{h(l@YjuV!f>1u#dDpfeUgLTAH?U_x}(GLh-4x+1tfNAjHr@x!)dVEw95kxN05RnUH^uoi|GshYV*%)h^LZ74P58fIV*p76aDZwG|_#QW!_}p0=$gvsJ2osd96_03H$=)&-X@CrdeQtYV_LW<Iu~tyVLHLK7#9qZ4;-*Pcz>b1>JOMDc$TmNat53xDIJYc5M^Dw0*>0DUNJjVq9$}kkJvfK1yKyGAwHKjiX-hDrHhYY!<&2Zljx#|S;ZVg^ioN<))Da$IbLJX~nYEj69(jdUj?~$R=Egzkk8sUDw^LUAyaNJjtnikN8*Ow$vF^-q=zQKs?-Cek1H>ftl?G*kvU;eK8pWv?f6%pTkI0n0Fw5gl`JaeO>5WpTqlyplc}ef@fAE~-vsVVXH_c1W_cb5VV=1t|0X;}293<c<yr#5w+9s#|b25Z3y>qtPK_kYQOQNbwRTZ7^Y)VHlJx@gx8s+*a8F?K-==_Q}XuWV0yEFr`<g{_=P;4TU%tZ)%Bl7Q*4k0fv4O?3a<Q;|+6~nzo)kjBwUnvZL0*^p!qdJmI6ud;}bg5<TdMNkX-HdeF>_G<W$wKz$xj9-$y(Bbfa{H`%1``C~pDpad5D5&rrV0og843IB-MavKI&-#NNiq@1pqYdO!C19g$g>DhFdYOPJ4?J^9~JO#87Ot<o;yIids-MFk73)2ZC%>}1&z82s;v}?r!1$S*a@|PqoFVXR>g;^Q^`Urs7{vqGAOqYJe>%+Yw-+EG>s&tTwiW!#*CX(O1i~DC?jPNyuh3EsnQ>EDh{Aa=T9UJ1+Wwv&GQUNe7kTS0LKa((4Z7T121zjpfl0&dZ`x_qvDVRxay1(LuL&8=itzzF-)u4Jg}fCbpOjd^X0;L0W2~|l67%k(>T$=Vo+?_Tv5$A=Y(y41UG~Q2e`z?4FT4RQ&e|RBHCd|QL$4&-5Y1G@{p&KaxK!5E%TQP5j1UfkyKpZ{zW2b&{M|nF-7A5GT_D+ZHTrK?BP!5E>Rv^FsAP^$yH^zZBbSXlbNJl>~X?vxd9uWGVEj4iz{9-#bUp>gw}CPtxuy@lyhdS{McrJm8vhbtN<Sp+zs3g2*li+KFIa)3LbM-DnH6Rjpqpa$eshpggw1_Cm`p1WrJt1CB`wFM?o}=&NNVRo%SS+fj{cwAm<&QF^9{j>OTKymQk%ikBsUJ*y3Tgdt>|+EMSMzbdOLwp+|vsUOe)m?2p9v|H;N9g+!=0>KQr8c$KH*Y%<r?ssLsvAJWiyfM>(&YT_)x`kD;QrV7y1pOM<jgEG|ELx7C~K;l+)4SKZ5X8mN+BcW%<GlOiHord2bKXyAHW9~srRDxIp+N?BX^pb?84M<kT<2{d;kBPU$R3%lIfVM<%O)4(7Y^ee-EGZWYA_)nxyH|#4t1Q~P%`n(Dfgxy;H1*&?Oe7Ytt}oW<_+=@tA3nUNYBQpl+sj)0@^UNV>Crrpb#XL4JX?J@^*&Y<X@$kUitQFRr&rTJ!DO?fO%}cf>w<DgB;m;fkvWR1+14?o4({gEE8Wl=%xhu0qN;ws2dVxPNuAV74@;Y#rzl%y=Lk2$0!CP6DsfH#KCvvaF1;+`hx&nsRg0V$#F?5h>h%=k>5NlSU^9&HOafGDpAzPl02Ew9e%b@KiD=REwM$hf&c*au@;d!jqx*taxluLY_<j$Rv$9}DmBkMVao(=hVIV+n0D!1tJ&C!3zazL`0271qC)?8{(2kHC<f{_>Y9iPeT5+-$lu2A2P@w=r9QwQ#I3P?X)FQ^T-oIXI3rlT_ZIeKvRXmXBBqjR&8i0$)3%i(2Jt_yplr%|qe*%=U=2;dRl{gOCp-P(5U}7!lm15H{&{7ai;mAyLl>}L*1N}`TmMz1=Kk}?GPjP-aP}i55(;F1dbGypazdO@R&bA&$j|_^GQW`mou+IEWE?h<+D$0+nfJ$)F16bpTlr{&EnP}RNy6H>s8v{CTZ8&r44@&^h6b7VXoK*8%TaC6YSbP=qKRP!sF_^HUkiarCF?=nL{jRfG@*1{|vr+&JPM>5cLTns>tgwmF#u+5`ssijikPK7Hq^*D>s>fkG|8C0I4VMJ(Yn_7>6)oLU)zxXoNsLF+`Kz4x5L5~0{QCmfkt-v<EQd&ijqHB;0<kg-f=W5`(<El5sL5dzs~%X%?E%0&^C)=80`vD%JMU&8SVk+6x*b!=C80^r6Eq@pwXS$)iIgomCZ6^kootE1cnlafIN=$JU1qxaOa+WiXzAs!KP{E5*)tl7r*wK$x2A{h9fBc}Nt9swsMe?6y?=--4{~-<fDXEl1!_1twmgaM)B<?k^yc&7v|!hH#s%n#kxTG7!gvGzOB^W;&<z0z58;V&7(B+I6q10?);q}xta<5gn<n@bNehx2J+(a@)w@P&>?&Ca3({8v%~*86zJe2Uy~rm3<UL*+(s(k>nH)V+9}V#BMhuB2)ULLWLu&(q2lbA}MMg2b-9J9u_Ez`)G5pezzt6~@Nv<}}U9H14>ian6S`{uO3W_6(dR3)VVBJ7%l{S)8iV#(Rk{R$UBXW@p!ASs5t`HQ{UmcOSuG|dqMI$Jt0Hi@%MA>g&!BaT4(H9(+R#C*mTYp<@uYIc-+24s7#0X>aYhVPayqNt}N5-7nzO0-5Rgkf-lAba}uo97&t6Kf=Sy`=$%vz4WIsJZg;C)=3;}}Kx+hr5|qwUxFWW(%nBG-(#GTWXj5*llze^|DnX&s+NqlTMMQxJrT$}?|{#e5#SFBb#7)s!`|Wr)K8a(-;*>%H0!2h2<yEfdBWu!?$5MS~Xf@P*FQHXKmxw2OGJgYxcoR{KfS<#5&QTj>GqcFn}}<KVrW3aO&ryhS5$WNf@dbPqN@jb51%+#hVpy1bxl{6OY5&1i_6Y0i<9YT9~Jzm(wLcrX>OEFU3n1Nvw8r`J?aK^TgcPkG<LHeUe!nf+2-upR@MGDhP@7rUVcFNqHV=hf@efnI9!u)2XTM@Ue2`%K!5-!@BlP#}dy!j4fG9W7Ybo5pJjYMl0a5g#^!VE9ayK7g)?>OY|}@`q>^9j(9a&66bo4^PBb21boJ4#7<t7PFp_n0rDL7N?hYCR<n%Jx4b4Z<?{kT>6W9p@^M$|LHhpQg@XqEUs4YPcM_62+--g*=R-?b;nX^nhxz4tNqKPp2uW3UywxS!e&gywbgKrs3MV2sHu7kq#8~15~+)H=!sa$Zs6(wTuAha*7VGp39Q!TkEC)DBC$sDx+?10IJ_Zgz7oxqHCRi**!9wnmP(H>Et?*U;}H(s6@|md#epBj51c4jLBjgJ;K8t<PRbMkdOlroF~t0u27!rdfu7BuWVm4+^<%hdIKhPKM>kz%N^hhN`X?U(G@o>;HVWjb4*4TYUEC?xT_Xr?T^IPlq-4b$2(Gz`uPnr`jRlQdN%PJTTY8kU^c0h~t@@G(!JA<B#aM$2YfWTnyc<%o0UOYI1um>!-1ZwlE!89|%1W5(rzzHn@i&^HL(0#){)US)qNetAo<YQpLzjm}WBp|f=AHGkG=C5gRLH<0x+X(@hGIo*Tp#hQ-0PCMMJxi=5dpZtO|gT3SAj_;NMT;Cpe$_MOQ{m#GyiYYWdbyYoK#AeiVDKiAXLKbr`~x^=y-^PBaC*6BYVWva^?BCOILVoEvlh0d726+$A~;J4bLFDBbZ3*AVOKrcC35UVS&z9GLhs(BIG)-m#y1|*co+O-i&O%DH9kJj#1Qrd*7F$*4Wjs+|&_DZFl1!{lm#KhqxXSRta_dwY{#^u?@Yc+B|561}+C#@&5jgpf4^M#*I?Gs`5EHREC$IlPgi}38?Z=W#4T>tRmt*mgHKYK}Lr<Nr&y0*cxlDOlX0W>58W=4~io80DN>t2Uz(bmgR!_R$*j5$zZu81YTu2lJIC0A!DbJm+$<xV)#06;gTNC<01(LRSlcxh>y-g<vs0lIO_xQKD_74M6`Hc*CA>q6+<Gd@kP>Ij-zqLAJhqoULYV;W+sZMBI5wJPo1G`K*}uey(<T&Ya~VtqRM!7xy)!RN;BXo?D*d_vw2GY4?&To+XakehqU{;%^yqL9hq4-2wooG&sAQyN=AjEhtv@lcqhJ$OL_B~+gtoC6%cNnBH}~wl%f|C)ox~BP-c%8F#HEz5nKhSqQINpJE|jY8J0F4F<#@GI{e*D_VN+gRpi`wpw(vY1dj$IE737Dbcq%kZkl@r&7zLlDy+Hczy<5^jH9NLWfAMGAb`9m(LKoOw8JCK1JgTZ%&@eeW)s(9p6`0ZAq}e|!S+Vz?6gShI55Y_CPeWVLAj~(o9T<O0_6l31ZQ8S+>M7e;gw@wV`aJ!_F>!uQZ!Nqs;aocVL>^KmgC*J^P2DO=(WXEGk_H@24}iM<lBL~2kUJr2u~1Y@dea-#SX0}(jBiZzzTG{k}qYPX^?`UhIV;=5VK=A#C$)`_tX`Dhr5M4SG!2-8;o_I4P7lmCBXzxH7Z@{6g9w5Q7jh(3p*GQ%^+2__3ljdwzFsEkA<2|EHwdrI}qpzH2FGE1nW?9p@0DbXjuaglged4UzI`j4rdw-(kw^IObP4`#yDsZy#nD%OYN?hcitj_G_tnI)*S=dEfTMd%nN0L2ZlGeJTT5RXaGT9x4d1{2S^lwbQSJdQeiXSr%*bF64i(JXSL8150FKiPpO%3sTk@(lc%<Vxxth*b6GB|;Iqh>V2I>@HyXv!rnIUF48HGudbdR1FUS0i5l##M!|X+(@*lDq8D+|^<T%<*VrVpbX!L3;v^M8*lv59c!jI|W@FU1>5s>$DfS03vdeAwqjF*rYM&y-npVFyY1^(Y)gR-G2NmQ%O@?aA6{2e#eIUu&~qkjOvv&SZ=1genp24Xt%aNbUJ;Ru92#Y>+N!_v?Xmr~C0Q(*Z(%Yzt~c6a(KNe7D%*IW&TZHYBH4j7nUGV_*F1<r-oXl)J;0*b6%;R?tIe<UB6I%$z=LTFmic|XSrs9!c<Y3jq^vZ7dss-JVsa3JBbwuWq>Ey4$7Lw)TLgohBFEXw4is;NvPoHk$bko%<c8}mSL8k#So#F5s<-@iOQT=PAY;fFdd)PcN|3%m_Ko>me=t2>hnK0i6&W}jc#M8))6B0`I$z~XRpOoE;z`0Ea1=2<m;#LWdPiN#^^w2L1Ge~-hZ2?9F{IA9AclbH5|JM!?PN)BzG&Xd$l;Dnr*qry;RJB&te*P9SjP@OtOr@Bgc5rkTh2V3=kPb%aGi61@NA1<apQeq!^5RWY&*^U<T2D<Z0Y+2^YMnH9{w~iWL#B(~gAHpx}+gB_W1rj4+^f6q}>hNiZ<IU5A3!^-6<UP%{?aH1=L$nY5CxXUG8@eRpkGHKk(tYz{Sk<jCZYX_-08AUaOm8a3H(GcY@a)|hy;PF&Pz{X1NLj^^>FT9b^oFOCVBaEQK3a1UzLra`T}&7abv85^mpK)ZBLFfzTwowc2&C&cuI3`T2ej(Y9Y{j^Hjt9kAfrAWnN`^{g}Mh(UJB%MA|7dOP6>8$fUj-<7IFL2QYIu!`6Kam30b*ak6$kRu#e0nH4i92q1JN1`{hxcBCl$~EprYL^6>h1pgkR6x_Z4iU)Rx<_8i<7?^Vw0)KwU1_md*K(7^>hfrg;>**NEAmr;n746@mFV)x)=!^A{36^4xW%%q-1mCb-Mu%^lianD(1m%(8o!KTJhQ=}rjZOFYvIhs~mPz_JyNl)#816N5$CwpxTml|rhVrORS=^cMR46}98r2qmhZlHfbUD)^c_gJg%p_WYPX17=>Iv6pi;oMZ>s5*3UYzfoX^LV?0eIK$w5@qDs0D=$f(n9lxdc+iz4cu2oh0^e&w5$DCfbvXOj}~qAa!;?wcC^z3njBNr0U}|ubf#9kr_%&y()*71PKpjPOyerwfjZOU>FcqFs%+P3i57>HjkJf+Ohuvf;+WDRh*9l;i=qqQMMvFr!>BcP%@lP4HKNa`SsZ#CVMRzY#o=ya+*<9tSptUCjKSw0hH_gpqVV0S){E5{$Z*OzRVKzig6+T3Y72Qg!%?R*^K5_51J64xw(~4ui_5(_Hww)gGJa7Yx{#DUKb1V<p*VLSRnDNg7_!cjR^je|ZpZItXW@{RtLYy@We*Y(>Rf2yM6ov4Wd{S;HXC?+92*pBKf1u#9{VlA(2$WFBjQ3&mv9{jijJMIeNKRoi1KIGD49}zz*&!(ECA(d_Zi*c5re{2$g7s=CD%&P<|0wI);is)VJRYTM@+PIm@g<CP$cs5a+Hb4CxkzYUi+QO<&COQxGS9K*{RNNkUKAj4>3?5=@{dUI8;|}szBzdTx(URpcu52EK@b`KpN)JCW~tAePw{Po#0SL-2G_6-MGdfx4pWn?fpW{Dg`V--aP_JLflM6RxZcoaztsk$&U;2z&5=0pPWEBWz17Tc3HZ<lNRy}>h{I%iJpaT=dErlo(!&NRR`X<6JR7tOx{K?-_K%-r6Hg&HJ4-l+q>c94g0q9X*Aa?dKVDCGCBy31P22bS9R$pIy<8ToOjs+vP>ekG-UEyf4Ch%(QY<mE@5N}pp-<;f9;aZ;Ex&Mmm%UETP4M$*WR!2K0HmR9Tre%d8sKs!;G3Eu@=&|oy)sXh0Ya!7nt5%hbysFDyB|Nxmm<ftcKju@=jo3Z@^qQm|Ymv+cBr5<~bTtK(&c!)u<B0k2;g<`ByKKqF41W`0w2Wt0Xl$iTApQMnfA!bj>-QYct7aIIqeH<J8HKl4&wGCt%HOSIoVxO78TfabXbE(1@g6jmH-CpHGZ1EmhciA&#hiM;`DXYLvL(2BT%ooq*asHp_FPL{y`95Z`t^b)ge^8}p`|tfWD<eqj}Iyi_#BX1b?fYbQUw!{_QR<fgnQ!dFSL9#p;fxvnFo>L9^c`vY(rp=?Q!{mE$=Y|fPau>w@*^Uhob)Pk{M{lGbI8F(OIA?h_lkYfNB8zYo-Yu<b4ns(|Qsw(ob%mSTaVIPe#3Z6B}<THeVDUAXNGOP7>RyVl9@pVN!mxs$z%!=Iuz&UQBZ2&ks<s-Er+T|rJtWtU+pHJ|vRTHbMiO?)BLj{pLsw2qUr>Sp+-8ZMEtxba`Nd^sP^Mf8{$Y2sl31grHkKj~tUW2Hs2nk3~IRUzdvlvAh9<?323Ld&&51{8Nn$qEr05&X4A7yXIk$L6HfJ+pdiMLIN#RBpaKRB;vW2c*Mfu+e*{FJvVI+7pUc}f1ZJ{7uBh1b>q!EtU<rTwY|xZo|grnaBcVnj=vK)Nbuw^La>C7V{7hoa*0=er$Tsd4xc4ciqCfS9SMm=UKPW;MPNs?$fSkad!G;+B;1S2jOrfX&Lvc+UIK;Ppx_icTdKyK)pmmn7tbb8L7jgP4OJ5Qm=hgF&~iSOKPn-e2{Qrq%C7`w6z*h4g#M^e=$?&@l;cB>0f5nh#?vPIOrFvPK63^l51u(t8dzC2On@`w=RM2wbb_L*-FVOg|UhFNd=Mid4D-GA=t*xx`U^z-;VV!`y#s2HbW9`AVZhpiPJz^J8b%p0MMM5^+=4wms!rhel$tROx1~hXF@xd=YurG)ZqKWg$nyMMe6C%_ze%lvdY8MFJPs@}tqDgRHJ4JippR@iI45r1q8lt5^341tH$L6#>4P0J9Eha}<sm#QI1S0VoLQR-oJC&h4kyU7B!Pt5HHs=oIE=#9e&h{jSbGU+RhmgyQ7G)}rDKFSinfcH3-GFwE1wD1sa6j0Qs<_IKQr)NV1a@HoDYPvKRCsx_i${5s;uGF)=_DpGJnNkObeQ0Nd#TfGy(6;4&OaL>Gv6^v6RVJlhdC2Dj)j&kv7D)=uu6<f23)FK>!9UD_frdJ`3N0Vf!i`C-@ZknoAm_(+R78}RqH2Id0R~?JmEhA4lE?cw#L0x+pN^LwrV{O=PSODb8!A-br|FrqTCBk}PL2}WU2r^*$_iYmom34}zhW$H1Jx1XArzH|4!W{MwOD2NuFTiGn`&Vu+sRutl$Jn>l;UOwTlhMlOSj-VLy_v%JYPuh>c@K;L0`|=MDY%Np8*3^Xq$dSxJh8MgAE1EFS&)r5W*79u{CeF>RK>*7q1Q5S@4iA3&AR>mvenpED)w4ulJQaEIIVL}<yG_Lj_7t=dlgD&JR!F{^2r?Hj@4wo%YoPHHCw6E^Oe}M8boTbv*$Q-wPi^H&NMkl2U7+H?L>7U1T~``Vao9AB>AzMD!^58hcRj@vF~e-g*4AN{%zW@ea4%ztc)CYdQnigDB#goMQJ#)<Z!Pz(Epb;gE>|vWGwMjxD+$_Wx0@GZ3{ItoN@8m(BPkHHkP`I0l^1fjS@1Od-OTLz$HXck6Nx~4Sy3Y`xLr}cSSwlL+Fy{XZY$sRa%jxy*{d;D`RJ=<&@x}y#}&;w01Cif;~S=x}<g6nr>GbfG1G@Fj@wI5zflyVr9FA(eB-%Z_6l+hMo|L*0rlW4C>bunc^J*D<SZF0Z@XBk9)Yv^RSQ?!5+bAo4SfyY!{yi$dFrY(Du*~GXn<ozJ8BS?T?M=?LX^wNpufVeRftftPf1(<0cwNYxDr`r;>hvGdQqt@Jy;c4V37dxevn}5Ax^Jk{B8liVz{E8<u5dKkV7JNtPxk!pz`y!onB$g|OotLNNuFY7Pdy@Nk22g?0*HGc`6RNO{(rwRg(3uAF)h_e=$9%h$1XemHZLX5j*BdM~5+@{=|50_R<^L3jFIs)El^x<<X$d&tU;_ra_=DiePS+bQ<l(5vL}ZJp_=zqE-c&?YfNp)L#X)rae4j&ccbR~Jka+BTUDeCeI3%*<d1wSaiu?g&b`(tg><az<u19B14|7RT+}j@clJ_Zg){YHufd+<MSJ7>gwI{RF2&$+t1D6DL0eIXhIgle5oBqv9DOW)3;G{WIOKt`<;laV_8KIvj7R76XRm0eMGc8OCT0ZnWKt;ye#bqFaNUaS9!4O0>$v9cKD^wa27rHh5tFB61R2BsZMTXGlmQ9@z(S$|%qyyeXhGykn%o*pOBNw!+4msTS23x1VH^EKMlMFNJ(UhcL58Hm{<KNUnOLTWVrX*W^Ubm^H!cPui!NE_`|JwSc|ZxVu-D$QBhvi^t0IuYzHDT}Xb-m5=_KFW-T6vpA~e{lI>zN)cP2NQd=GsC%lUVof2OXl>1A^YL3=P+K%RpyyenxmT2^63UPE*Qn;DoNa}3>TOSIvr)|IJqMUVbJ=mH_3-XNf1ksl9PSp#@H#Y^rzz&X99tTjv)bT*cYr(z;ROY0YMzwO&v0$uB;JNSn_o-XXIK>!^>)KUFDV`_b&H4eq`6?pg#yF&J8b$2#U{je0z*%xXHWnC+4XEEvfX;i0V0@u*T%Y<84t`Qz{{bhbie$nMvVH^E<ry@2Q-@x3iB$5dkU=AnhdFn?^r@y9YO=C1bNxb9V)01pv{c%2%LKzwR#5a0JfdYw%>UPBlrL9Ia2R_Sye9p-;zhPg9lLo(lgt8;J1+J;-!>-zSLcm-^4%vA0a_G8~')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
