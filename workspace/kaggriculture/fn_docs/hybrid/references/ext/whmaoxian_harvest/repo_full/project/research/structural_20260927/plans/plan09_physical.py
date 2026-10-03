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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-q}vQE!|_a{MoR-UpLQ$#ULkY0nl;HVsM6;$jGffm{$ExI8#{3+}&%5xKkHeqCKv-7_nm^JID{?l<2|&rEl9b@ea*bM<e({r<PV{(kjOzg+!v_u<3Ur_I&B|Ms8%`d<$pJpA~#-+up(zy9~b&%a!K`}1FZz5DU)4|ngbHdn9j_g9<iPn*Y&e|mra=I7TRA3ooIzq@<*?~6~L{=PZ;>bI}|{PRzXKTIC-VfXIc>1#ee;QP1lcUR&EGPdK#AHLu19!9WT5AEBZ-@beE>%+T${Q2{@9Y?kp_0!*e{!;$o>EZF;@mF2X*t@&eJ2YXxT>W_e{^R$b-y8k3-+lOa^+`@ET(|3V-Jbrz_G}=JkJ>DLI1OVpt<jeB!~e9~y*Xcy^;*FvA7;*+cY7|L9<{WO^^-Peh)>(<m#f!zcqTsl-+OMZe%QUc|M6;b<Bup#(BmUEcxbETS`I|M>WBNE&+KcHFNS_W`5J4pyT&Vg+H6n1Bd_!{Gs#^2`0+Tt)uTQyUTLZpTk-DW?md4*d9v2uw0Q8-JmL|k=RM7Ic;4X~;0wmrI$Fo!SC8N8?ZNY*#7ks#KP@eq%=FXm)SF-H$1y`G&$RKp(|5*`md<bQX~|c^Pv%c*`0h=dfYLrZ{qgDWilz(ZFWGU20m4(UIcIvadDHVW5c1WBp^6C#Kh?gHe3A8)ukYWz+r9qy>z{V-KfZnU_Fv9t<J{UD$1wY0_1HJ>?|-^-eJnEk!@otl>UiA{2W|1%E9VzF1mUpe(-+22@(I9dpQa}JV)A`)&f}MmITMcR&G|Q@c}YLs-90`2@dt0EyafUVa@rop=O*Kt=3aqE9)FMy4|s)xKNcpX@eB2M?JV9T7iRcoxR~3OGm`pY;UYV_U*5ATp1)&9$A`r=jdrZRj=YWDjJc1R8Jy*6gWD0U{puTgUOWmc?XM#f5WK9DGkN@e?d-&vIIdTG`_9pR`s0&lefUV<gTTv6)+A2EtgqGH7JKc5XSe$3|CK}3@`J$EVDOU+#Ix&u`3d#Hl3Q6?4|pZ;ZiRC%JmEP0{6!>q=iLY`2MEmkI*j$=7J?TkCo7%$&MW{#OguiD84!98O+&o+0C+L=&5@6F)AP!_*^rnvKu{6Tx4O9SRGCrKZI&MJhXx@1(?{vZtkWIb<13#rIf<CXte)}x-TQyey&G`PpME<1sbl@@d<8E9Zdep=E!^Y}AK%~Yzumom{}=0YUydHUW^_R3KAt23h!Z?_3=t@|CPIWOKDHOX8srg(pXxm}$LHen*P9apb*+sX9q?0vA#<juxzL&0S_A}l`Eq?Bi14^#mvWMu8Rlp3o7ZEFXy3DW($v?S?NyU3r|DJ4#H+mhYlva;aSuc;dXdrZK%=S6FMgfWJ!CGe#Gb5NbMBc26RU!@!Z9@A&YR>)v%JEg0Rqo8I$Ot&fJ>K7uN>lyJ46E9om`XCbs2wmGKn*<ZuJlSId$AAhOvT~jVb8Gw;Nv7`B)0$q#1eu-z~NmaYy{;!vNzn0_cW=6K!M&B$*vuzziw9oa3Ll`Ij3*bo}F6g8*#qAdVXvJn1x?37e&`apN@Pd!_euE2amh26Ns0r#~5%36UF#D&r{EnE7yIV#OhU{HTHX$(HNfh#3ecApYv&Aw&Ae!H{9`1m&y8=t4dZoHz=17I^@PwkfK|8NPviX9;}|MW=KZ$Ll#wMKo*;zpz7C0OLB&1~;7gFikW(c`TUAKy#ZGV-V8C$-_ALG&+s2-UiL9HpjK2gSGTS*Q<N+z#(#%6Xr{Dn;i$=WFp7Af9Zgw*`VN=&7COZD#dt(`4?Ym{fGw#MrB|;lvPa@%V#%$w;(AA5}8=G2Z^g$?tz6t!swjXGve+H5it^5C`7?mt+8^g<N|vHc&8RHPXYxHGS}8=ic4>-)anAg{jv_d#Ui6HZOO|ezC7|N(}TW1-l@G|`n$Tb1m3j-#n;9p-5-#q;tsu0pd=jnbomxko4EWTtxrY}u>-?+vSkQy9K1%n#g7BaG8ExrabuiIL>Y@iJC;$xP_V!?^7ua2Nq``y#m=G_=@Q@NjL~3s9Pzv`?#r_ocpPp0$zWj!mloY~tvVC-dLWq9&tUJdGiV)g{`@6^{zj5>JH_WJ%R5S`Fm2H&6>y$gDefA5v!N$gu~CCNs}mI^lKbcb#(Zj)!mq4D*!lBn;!<UWKtBEYQ;lPYZa?_p1z0m%1D9MvL*@{M{K*LX6E?K%(1MY0pKE`A|L~uehh=_<=-yn_1R$PXWN~2YJ6-~+Ss{~phf&za;Th2Y3tY4G70!Uy@9ytE>}n|S@lTAoG#x%zBE3q@J}$arQSs$Ab0`lgRsu&W5J#v0)(h7yOn+llV?^_a&Aq;V+E97Cbu>k_qR>vj+qVf*)~dF1GkDa9Kh8*Ti4A|*ca968w)5#Vk9N!67rgk=p33m}x*&Bp>v4RGAW&na9X8l3RE{<Ljk8lH9Z_<JtBnlpqH|uClYyhJ9+ygNZ(`8PwOp0U$^$Up0yEx{aSY<{<tjxFFoJKyj;&iW1l%i=q^M@c^hT;#0F#NCjx1`+{tAuT;xSvrDO5EhPaTq>0hfgT(cI)H1Bn5?wX!fY=2(dXSED@jL`-M(02KdIFQl+Gesw!jFrq9;$Djetke6~A6HL+~CED?ZC|%X?!zjX(sttr{uZ*ooO=ethi84V+7W7gS#{jTSL6XW*fLqz)7v7*#1P_i<6){KaZq4*IGG_+ab3l6NwoW(OI*5T?&aV)OcH%7_JE!PEJd<Z@(H<+-QpGa~da^Q+Tbg?#v2T!0f_WGWF{r*%u=hkNbEp<c?*v;VO<>f1UUguHZz~QMQUH}DbX6&g5`zGY2z-Q3BC6kbL3XeO`+~(s=Z7umvaKQS$3+9P2?nVTAI`{arvAZo*re@HhpA6@_EGmWF#z8B^vJw1Kv`b^W~+yM+SsuWYn?XVD0hGoiM%{`ytsKd$RH8$k*qY1movJ5;C|jos!o@an?&)-Ltq*?J6HCPL0B|`vlM#fQFo|TiR9C-HR+FF1Z9@G+m6ECr{O|RiHaA7vxMQmb7vXqB^%`JL1mC!-iSXx-?8K2IXagdwGwL%0Bz!ubdJOk`r+-nKYvcz^6(p4D=_sk5B6xU$AOrE`L-l+$20c39IzkL?x+%HkJ}zAHPmS#9i|`Al4aL3-M}i6p3DPJ=N%+e6WmrQjxZpOP--eR5(1DT<EH2w6{70JHca2aY}w)YO~sJF>JGrQou&UD&FpA4DqQBs61_z#%J2q0FDnXAECN52TP5~Buq!~*&9i<x@1?22dh}a47DdgrFXWSO4g5R{YzHEXdmKDvE!d*Ei~tAOZVKk-qXj-hI+w`mX|uISWgAY~oxtrEJ{T$c=_Hdz-Yz16$mmWY^Arf6{R#&A;6R$e$|54-LmCemr=Zc(W!5^-FekoFo*mAtkJ#6xcTfVdalr|n5la;o(gS1$Lj>4I7(N!s%l@ovaV*1f0ZX)(C&$<;w%8jkH3&d`p#MHSIA-eKGO`1aV5u3>D2;@wK*YiV8Tg|4kKfk;h(M(+`GJB%Ye>Fd@{@_4Ulco<Q1EkOI5bn}9ceqwYH3hxi6aukcH;b&M)bW(qN9a@456YN!%j-aZ$3k&RC!T3`yLSv07e3sE(Yk9%Fkhxek)^L!GNqnonPwrK%XqdF=xxO5&svY7D4Bz<MDf3T*GeqSdBDv-^*aTNZ)*E#Gi-F;{_!?5Khs98)<cgHg%2-g44HBO(-%IZ{B`aEQBlj#nMvG;0;PRI?MG%?NW<GP!fOn!sTDka8nThMPUFi0;`^xqUlgjV_`8H^A@{}gb4}JkA8ieo;chyL=h?FYSoM!r1m+U)SY6+bxMa~X7o8?+m5m{zY`<=VCO}?)9H5*!ksa{@g|nEONR1-j%Q?9rf9#$y-slf`BGe&q&Lf~EC+!{s+x`UshDTVJm%-HI4sI&m9rH9j%5hNlY_v?=h?Vk-%A1%(ciJ^l@zq>(sJCahC|71k>cfj_VvY)7oxxiTVqVtTq(9KufD=DK4d!JjNgp=PS`B$>umupqDuc117LfEy}@S9+S+=Ys%^1nhYePsL$(0lvAk}n%z)*zj-Oyg71M<-0mgAu%dc+2KDhA>80XouY~lJiW<=SK9w5!lA|JvRPnQTMaH##D-b#YIeNLZbGG5luG)Bum{d7DD!AEF<BX6)YWERkzW8hCSoFEcskjpvPhZlq;LgJ{c3}jKZ;dJLHD`I6psxC54#=IByfdIHpU~~9&Y^(w93X(4wq)HRShn$-xfsiaYH#X!af@DE99z>hx!<A|<!3l?Tt2-e#Hn4Go%iyPFvD%(baZWxavSeKwOP(Z{*&MK<flJ(;hR^z<g`w^7i4Ivzfew{ywDYTB`G3vGnNS-{8aMxG^(Nq7%nSJ=g`1Y8Q`-T*L~_MVpskV|E>AfedOQj1b<xCDz}6gy!0`6heNJ;Z8g!^rB%ZMj3023EGTwdn-PPt*1#|0Awagc-G=C_AH7_qNlzUw(7lgEs4w3`E$a6eD`!+WfK#H}piO!ekdlvDI+M906-C{tT8>u9Svg}6oW9VnMavrgMq7%xpl~TZ+!7%XT1lWxBuvWK&$Broh3fLj_!39z<fzLO9{!hdgkT(G_FxwF~L8@Ak%!hH%t<4L{;$b6=IpP9(ZxAmg0p@C5<&`PN_+Ccv9-$&C-2wliQrbD89_HvaL!?vsAhhTNeAL;Os4WKtToh=8x=_Y-ORG|PHNWSE4DemR(3HqoU0O&-?@_^kdCGPji*Wyk)7Q$-O|fg%s#NM+YJsA9+z9s-J`+JwTYxI?oSjN5p#>Zc1p*wA1e=(Ng>=YVIpI<MvuSdyl-t0|8gX7MF`{Wa6Eu=@8>avccNF6%qf<T(pXC>$q+=KXI|0dPX&B3!F_Iullz)ajUVQ5Ht!&Uy#;^{rCg?Gke~~pu*?!ULAjVE<105-oPG;3s4M4a0t$;1W{x>Yi<fIcsq`=`0#rlY$Z`@PhV1Ud6zb!f2bxDm74{(c7RF8Ne4m=wqVOc>y%O+&oT1Y8l$3}kDrK;eOBKCVtT^Bl?IExzR5wIsnrN7-n>zJtX@$!t<B?@bC7zo{uPKCqiYk1}axCBIlQ0^|dfsmKrVjDc&z_Jo@|HK7G)xo{;GZle$)v1{PXD@%xq9EeRPbg{0+<ts*xf&@#UwDqJOPcdjsd%0{$w6~BeAo=r@A*$YO;5J5D4_u7@AdKihr5sW#duF#WN@Eer1l}6hRZr0eT5+VXGA>)%su4_wV#Z_I^bWOTWvDs{O_ieokE9~VhbBnYhxUgpb=@NiX^NO&92pa^J$DXHSrV=W{S>nlX&6Hm<V?W$lBvqY@`cmPNFDwp^NMlY+`5x#PALp@$$<R#$+yn1vK1xBAawyY!l?=rG6ViQwD*IEsoP_`C@_&l%1ui$XiDbCV=&t4`Ak$2SVi-AtSK}!GE=DMM^OVktd2ImwhgDvjQkeF~$_Q2K8Eik$+0Cp4P}`Z}TUV<0}f1sz}J%_*jn+Hz`5)iFO27Pi;GhcjB~aV>B91f?eY?Qz)z;x3CS%8RrELda<%q7g``So!Hd80&GyP9~Wwh;v7-*bHM|<bR&Tjr-~jEG=Tcw1<G?*T9HjZ*Ir(qQ%|8hIgICP4bZMIdZtx51*tc!fg2|1kpRDDe%J|d!C5{JvLPvCnV64@valz}qVxr?dYhI`qK}89TW8w5t8{^B7o6D%H&ZQBU>47SqkfUv6}--ogq5jU>gt=U?bwb^v+hP^45A=fgMI=RjR&H9{@|w4F-FF)ubx56!{<Q2NZD@AiqxaMDE~2If4#Jw(<dgB5knQ9EkSaPl}0_Fj||Bjt9hNvNYI_Hdv&XRrHG%vCl|ZlpK$Nexe-)>FZs6Kgk!CK;4eLFIc+sV6>W_<a^c))`+5nuE|GBkWSr+>m)whj44w#x;pE}KsIV(+xJ({Ko?8n(8WD6&)N8xR@x*rrP>{Rr;-aQLa5;41AQBz}jihBpS)#9^!qJMP`P9--$?oy?m<t+c9l^u~e2c(*ZZ4#Afnb|*l5jIOvS>R?S!Zt0?exV}6m#rq^lHn@H}QIs2yzF}c!@P@a5pS<S8i&v&Gx0Cc(MCX<Z4lo0J%>^k&mFd=E!<iP?8>I>Zqo>P{H$;?C<35K+YS`6`<6q5yza_8AsOSaWLlGTCcxa!vznY6uOqVxD3w;d5nwm17WjfVr;yA>t*zV6+`^vlQoVXhL)cZ<0$@<+cJ`t&0(sx)%{(!iaK)s><*`-1l86Ks`XH|0WhMgU#Vi5KpL?!^b~rbc>WB!2usd~A5hIzB<*EzOo3Q$cX(EDa3TySbW~e}qVzT&+N)IN6YJL_(sbhTF=wmyKFs9(;)qs`ourgTaMU=*>PSo`8~ZP0*H39Uklm>W-IDdp`7UZ4G?M7wtB|n}#nq#RiD3*YOaQH9D87}r#1|LIvNwWPP>@-Zbwb4(Tl&aL2W<KI3+>>mqzA2XD~L-f5at3{62bVQ3rA^dxkSX50hKa*&ng(%0Zn&kZ~Mt;AIo^r?ZdI0Qs${rxMS(Y0@|?02FeOMYJ`sDer0X66!e=}L#Ojk0~+v_Qx)_%c>ov+v93;{Ndg&h#q3BA0=f~B91$at8a6uyAi;UB>xB69uZn2M5F6&3XTXF`c3{(D>X3z_`2I+7xdAXwtCR=qG<N5zAr}Nuy_5q`R-^iJ!!<ax$&W$i5$<cH56iyXAqI`PQL009jvO~9i}moG*C^w$)j&O_rJX&Y@-dG#{;G|F!m0v};1{|G`RQ<5;;?e)rNkRiz?2ui>aEByAVpw4u1XRnLI@+rICxEXyC+1h1uHrbBWH%_{#YG|=rQgCMGRF`0kVNTvAXEu^vAwImV|WPcTJzBV^}}#&d2Ll%p5?y`NL$E7Vj1uF(Y=sej&z(zbBC0YpR^d9$CZT^<=tPofdt@tgxZd0cm;cy!_N@bde!CthF%kz0#t1Iqd731T(yC>fM-vA)-?yyJ`jdCNUJRZzgnv;H$v9t;T7#EJVe?qS_LHokYR9+vkVa2AFQI;fs*}a+F!Hg>Y1;LZYO-9>I=PLj|Gr?Era_>bodNrC*g_23XF|(L|>8t1s7`MpG|}O0A}<ih0#+O#o&}C6WqryQqgbd4+B5l!%zb7^RsvA*ViCo5VDE)VDNX88}T*L`5<Lq!i@&lJzQ-2!<q=yY&XW!X-dwq5Wr++M#nc`(zs^vPy=@KbsUi`hu!fL)KPd62k^iYuxB9ym|XwBfNIBc=iUTM%0(BR(l3WL51{PTbi>SnWrkDd|9=`+rZ}?9cNTNZ~-F`g{3zJMBK~q0ra?e`!y<#pkQddnVdG6d^v5^m~k;(q!i=zEve^M_a4<~jWj(h-23~F#dgp%NOXo-YxYE^(XDF$krYLcy4~Q)bK^*F)drI$K6Fngl1|Y>fu}_(W8(>#g9RKD*>Lbam+_Fb8te3Bo=J9i_6nFw5+1w?KR|gXD}UH&Sm0la7GW$3EcJvnt4)A^+Y|+%41$Sbq<%z=VK9MD>yZ*QQd{tY`^eneLrJlw+u7|Q!;_3ORBAM!;9x#=oTTdCaHk1Ib<({Y3L+y87yvKY80`~feV<<HHv26yvZhE5DJY!F$+&N`{nU-0A?5~2$r(ZFfH<&Rd4<+XaSjH(5Jmne?Q^T53``V6)IXT<yd`+(=_5&{ypY`XYe!zzvSiMJ#@brZUBKN*j_+-@^At^R)%m9ARaIh=+2flZNCd5@5YlD)LS?J8@rzg4R*U9oxChX7zU3!NfZ#dGLO-UWV%E9nAvu*zx}Yd+%G|D3+v?f~VR3ff!2aNGKpDiQ$4&9#|CCR#v<(3sltki&^7vDsgK2sDZA({UOB68-(Tv2V+DUrW`NTvC=CwGvY11Y}Pg@leH*tpw$N)ljE3<AV>MtW-VUvUXwEdLKmeCDIvP}Y`W2UglcpugX?Ks7jX0rt+q>t7B8Q{E+Y2ux*|Ldf$!CsFH{IaAT?R;JEbUAh1=_|qeRCd}Jxn&DH`!BWEt2uSjeZcMkTdDiy(g+Q~WiyA0buwf5?UYcE>%Z}gv`&`k{hIiy5F+)231ka_^3rw*)O(ANegMtJyH(QV6)7IQzJl#h4`=#x6pKf4nAb{5*X|zF+-;6Pr)OKvh1De~P#QNAX0gKDo~Gu`8IoY1%xJD_Vx;w-6vk((BG4`(tn|^Pdw8mvhePVCNF#rxAb^`c9t0qZcE(zWSd~f#E8ZksLM2V2P9b1Y3QESrs7F}If{u|1hC7U?-|y$=Z*2huKc!fU^a!zBNhb_aZr$3#IyBVe7ue}r+)ZGVK@8&9o{j=@FnXa*G)EZ*`tm!Hd{%FJN}YA8S4M=6Jm2?%h2j-y0OrM+B9BcFW>0i6L4LuZTh_cwAC8oFIy%<`o3b`mE6_PX-9&=RWE&Vh@}_3o1r$eBg;Efay<s<B$vyjc5#lQ#)ZvVX@MY%3;UhGhXf3qW)7-8JUULGb6J><SEi<mx`Ln_=PrGA%HWml~z+CWopPU#m#j86KH|h=CZlp{o^<cK^rlF(724=zi-Ya_Yoz{&<<4WvLcW|ZhI_VKh&njFFK8K;gaXBg_8Rnu;UvWDOMV!9(k4HneF%slPI}csiK<gMrxCyp^K#QngA`{zb<b<2V!w^leOv$86a}Wv|lod_0xdLV}2V5{1CMna#D@Z(DBo<I}DKvPPn3>(XVi!zBYhKq>Aan(y3KV|k_TEJH04&KXNgzMpb9%?{GMnF%`$&c2l0EgM`e6uXn(L0QS|?nSAR5Str0y!APYw*WN_L%|0Hmcb-Cp}1>3s-VGqn%)y7}-X;TuVkY=7`P-r~ov3I|dK1F;vEMNQk2veIs4A=L<;p`u`YJr+v)G^Uw(H!<r=h{)ySsZIeO13;H^3Jj$jF3?HDua!&*0HD%~Oozq8J6GWGQB~2>mbf4$mJt_8Haq7xX4f8j4O2pa5+odk4g-<QW)ZO}B8u&05{1K%#X+z4<um9m_}wMP2on;mXbK^^;DxOmz^**yA^VJmO3*^21VGRNh##_Q9Q;iixd7SUp6FpsoJyyCh#YHQEid{dmeYork<I9T7}c<q9QyKd0+X*$%Zu$ED)PykA>+BXjxt5=_<2&owN70G^kAtyr*hTlyFyO&=;s{H^9j95K`AW|V2r<A|F_4=;+cLy|JiAdi}T6nH@INdSh($_o^Dq2QacguImn){Nk*cx74E%q{45)}@Nh;o1O2upEb&_w>@SzVsQQxqnmWNZ8`}1LQA;l0#}7}dC!f8uXYcR`6tU*MG~1;RrXts+RJgJkIT8elOBLGaN8{B*f?GoKN)Q85)pbMN7FdfnI4reeIeDr-P_Un+tO9|uq6QD8co}C>4-@jVaj0O1<Ax;elZH9YNgo?eWPsHsX=QiaF3_qRD)r)PV?k3IUp!YC%{YaHFz*gCbUW1hf|Sm{?s_UT_NXgx!shc?c-@VyKUtM+lF@my4}dS`Sx`#c7h3okY8>2~*yp`7d`vM5L<*{zwz#KF6VYLu%->I}#37s6frY>kH797WAQ;fMhD((CmErK}`Vu`79cl1J$xB1+gVn%DX$%g0(#B>?khib`?F^>qXYXgGbA1PLlFf*6M0p*-&x~9F01T0u#{ieb;W+V1nv&RmMf;%#9@ScKXSY^jMEjO{arSWE3lM!L$U!^<K|*OamMm~Pt*&p98QYQMB4F@qt7>%k$CqHAQGwR@(gr)lztOCsBkwgxuN$(2vfIwis!+1jGj3YVbHQ40Hd7tDp#>C29gRYdso1G^K<@+fEUoL7zA9HX?RUAcuv8`G8MxxlFWR7yEa4PQV!*Gnzt6L|%#^<V2L+8r7(@~`(i!*)bI46UU6wi&tDrj6Ar>l`;L*Y!d@hlyeR7#zd%LIRene8DUJfOJ2<^;v)mmv)yRDjN&@_#Lr~&2Hx-gF1=K3hTT%A-M#^6=`y!szUubPZTaSOoXkx4zd4_KO~*(#ptew5m7(yn_}%5bQ8g93U%Z)E26tIbQCRmLSb_Xh^UJOEJEC^4GzBR2t+tf(9zstUhV1EDhW0!E;vO#m5yvtKu5xBiaCCms0Em{8FNQYRf$NmX>!Y7Eun98gPb^ig4ajzZtcN<|%iz9eRF$-4o;R?$D0O;t`XdTLpFru55dB*_7-bv88!Rq3EB(o=hfakY4T?qanOLubXJ#<C4SnK~nSHhDH-F;A{mUkrtEfPV@&PxDUR%Hx@3weSX@@lA0fJF5Buq>(_sPfU=&!6c!YX9aC~ydF*wR&1VLg%_Qs5t`4#zIeSm=8IqI5(em&HN;X=1bK|sv&cgfS|!_WG+r52*HvktIaG&zK-s3;^+ka>&Y@TDODBTYDvAbLixjHO!Ob&T;+7+ue$k%ac3Bh>QliM9a<5V528m695M4yz+My3PhiG3zU>r`ZH%Fp41;|4=+)6m9^Wa2lENxv04Jw>fnn2C$f_jmj&R<s(=x990I$2+r$*3}`sh2#C0a*~3Aq4}+FvyGN=CySRgBFrIs)%v%^57$16Ma;|yVoB&@0%@)oOaR*bWMb__iNCYSRxATu}NrV0Sc%YgTD$!2wUIvSQFLg+}3hB{lj&g5Ik%vDptcy$dDFOWVO)oGC3zhJ*GX;yEHyklJVdT%WZX|gDQ!OY2&fd$;m*%8HHu+#_(<dq1mAuROE2);VJa2y@}dBw@oT+e%clqZ2I|6(uispjye^EJwJu$W`sh7h?!&JLkGio1z@RH&&wY|9%fz@&;0aDaE7Q0$opG@d-763L_qqf(uqW_kqX5J+nIv0Ato&82Zj6HsJKJg_`XFN@}y@tF{g;nRE3nI_iWUnPyzmtN(dzI%Ax@<ON|@7o|`7N-AwCr!GP!LCB^%9M^X{ntu-Z{G=@tfP?@D*IEZdd7f@E65#;_YHo8cwYt^p0KjAzpb6X2KIijVQBx{Hmnn{iI3(Hc_g&sZ>Kc+g?4hmx<u<+<Txo=h0g<0Zd<=}0V6X|r*Ue%nrG0K;wcpZ%dos*w%)(JB@Nh&~7K)v*s3f0E%a>lTeLZ}Wgbnmw3UcJY#+v{dVU-iOtj+A&MouIANQsE}_xdI1Cr7%0Mt&7m05IN1)MhE?3uKm2<p2*_aY$R}+Ds87Tld0B({dD)?L-T-6F89M1uBl6G$NrH~o9$GQAP2p%BGd)Gc`=D-KW$Izypq38CZMhx#7Hb|{~NoRvX3=PQLM3>;UE*EtI{SsLD#?%kG5*gG+CnFM$Ll$K}C68OB&aYbFE$@JA6_H8`qTP#9!h?GI5eLUCYjQa6fMgFp8>mVQCE2LB7<7+C5=Cr$P!Lp*`H`2>N)1m~0hc_l(mhb%;t8Z8ZVsN)J2546)cQ#m?Kgq!jJyyKCv|N<!01jo@VfRzY{p*`Xr8IFI6x1iF6vYjNUJGFrcx9>Mu)U1m(34g@ubtfJIm*3Au^7eMX~04luG1c^m!5;ItBWy@)2jd_;+6lzj*lIJM3azL-wpONBG_npR@z{YbEI!COatA%E2?d`RaaulJ8CdOSXeF*{e9=+b^eIQ-e(u`SDt2A&)6TYQK#)*!L)V{3puvIP9HwkRxED5EZ^A|xxk%-x7Zw1WsGh;R9rA@a3;j=Akyf?)1OD8rU*!Tg@-aPRdqBZPY4*4QSS-Z9l5J5vHOBac$D3Z8MzDcQW<^fdDr9s|ICP2wDa3=Y33JDjS)v6pz#EFzvQLp%sL`_E~M5?Pbc{*A#hGtr8homoL!mIjSea|KnYD(fhnNF2BR$)kW$(1&Q5J;7QThCwL+sd?d&mcfXrwcopAw|pM3X~KjS{vw^-;dX4mKWXENRSoCn$}BZO_fOHX>Hks#ZeELg((&lf%f<nWe!9NDeYP_No+<Rt&0qOh&us?AZECgBdKItl{ZEa47kAPoXN8`{`e0cexm^|Z_tb{Pk82qUezuMVoy~gz=X0UdZo5d*`a!(u7O6@g|<pGTm~e*_^Mt5rNekfdO-nrhUqP{(xUY@)UEt_ZA<aq2+kmX%H`XGBYr^16E^ec`w>wK4C*>6?gv=pynFkG{GvcKXNTp!p)Mksx)ltPj3nu4Z}z&!PTElYNhvQTXO`S8#)Eol3NCt1?U%;1mCj@;S<A~rt6mblC9EE@&Z@eN09A&jbM=-&KF63zKy|#n2Ib3~E585{Dj3X_I`%wsFjm@pRuMB(dMdqszo`sM34iFbn~Pz{1STB`XTZs;y;2gz+qydlzT;6Ql<C}aOUIdY#$;V$Sr|gzr%_%BT=_oXne`cnp-UY0>XS|!Xr}#K9;LX4sQ>9lS=VtHzIK;^Q9J6Xwt^U*Zi}oUU)sU|>_ZTF(SI+4^IJ{Za5~LMZEI&+E_n}*oBWhl_6|B0s_skIY9tFRnw~iJ8pnMqlQ=SC!zWgR%_@MxAoEW?{r%Jb0!Do5Jp')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
