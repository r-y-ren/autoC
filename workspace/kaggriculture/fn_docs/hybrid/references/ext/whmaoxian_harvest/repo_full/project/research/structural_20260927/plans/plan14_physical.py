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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rk<U5^|`a{MoR-Uo7axuX0=QF9V;lvd!!4bB1~2=EyOjPrx+H^cwkG<RpFr!z7lGOK#2gZ!k`aCf@8y1FVeG9vQl|9<kXzy9|3zy0>)pMHMw)5~}7o_xG|@^8QX$G`mNrw=~;`1fCb`}e>7*QcL<e)7$Szy9*_$Jal+eDmb$$*a4=ldESRukJto>FwROA6~ux^!efY{mW1PeSZ9x(;vM1e!u@|@h63U`1n6p7o&Xr>dzm3T8tqX@4Nk*H|G(3{{HV@zui9(KP0z#|L?1zeDmS;n{R*lG;QxceE#dxNEV}9-XH()d@<|y_}#82?aj+qdo*W1Kl$<Q?fdUP-#Yr~uz&Y{`H`GsxE}I{`0xwY7ehK-bba-!IOoa8ykWe0xqfc(>yJ~nd=}^7kbjK>dbi(y`{{Ro*uS~^@yXTBpRR{_SgtQ{-G{qD^LPJ)9?|N$fBL_FzPN6@Mw~G?hd;hQUFTvPt1IqbuJ82S-G{I$*UK5t$KmDs{abR^*=!%L17DKWtrT7s<H~Wq&rk6FW|mipLpgqO|NZsneVpsdg_hp$>T;K(Y)*b$>gVsI*E5&;X~U7%T|C#BbMHU<c#Uv*d*&~9>Yd&Q&)<jUVZG+dce{=?_`StrV05<0^~uu?(>>w351-iY)vWnGU6)<$y!p<%F1g%!Ov&J8JZE;b;}78R$}c|875eG))ej$)zM715^#l3ZS9fpT>|eeA<xl&!?_a-p{m-9gAqk$d067UO7hmZ|mt?5)1g2kf+UZt9N+PXr4Dd<vLMwf!!mIGNZS|$!zP<Y?TYmi8*}_{z<-6np4?!B<6iV}NM4S(Iy7&Rzp9*!1&>!4=^5Omc%iG@hw{0$Xbm7*$p2GOk5BIZM{_6O=KsX#H(O5DvKFiV_vcTh)JdFS1_4)k0rEgjP@zwE**~_+y?$CCB8lBwSkEa^?mh*Fv-xBl8`j<F2=AT;Z#{6&bkJLZTmsH|`CYUxqXeb5}Ae$uEQgU$mVMZ~S09)nhhe9k6F_Yv*vX3v%02k~lL?owxVI+#%eJt$5^olyVk6#_b5DR-~pJH}O4<n8>f^BT75r#ewZOWa37tXs?J$MM!GzLw>u+!Ik|MKl$Is@n54s!1Ezn(6c259fzzkPZ5X8-o>U%ltOyoq&gdWAr@#RZz90QV1|VlbA~WEZ1_h!r0%aa!Ok!d_kBJa2H{iJ@C~utw;#oNIBN(?%B`XdQcvvv>OXEGF$=Ee0{!S8sALc8vg05g1Bm`xFkUY#_e_VCXUk_-ZH+j1j{hIPg1v^oWt)>FO-<d+a#xSu4&%(S;c`85i_GD1Bt>6A_$A;3Nb`$xuKD2EqbD6r$+UjR$VWTRT6|)6OWd6k5EC8P)Qr)M$@2>eIRioBgy{3B`)>RE~4SA=zg57z4LMh$h#|r8g5W;EF*Vn3MCPu)(-2@In>Hco`9!ROc8DO5CYD>_L2T{z8}(oF1e6ZuqD|5p{Jt4X{%_Esz9u&`=+GtPP*kzQfo0v)?Rr{(i#48Gs>pQFB^bi6UVE8g5AWI|we>WIR@wIa=xDC?A0hW(J;s6hr5sJ`NBJ063CC$Q|G$B9qx|<<QkU#4?5eR(uL3!$=<EWW?|kVP%zzaF!v3ch(TJL4B=NoMF`)!Wifm%e0JUd<3>P5QZ~O&%k8G0Qh`Tqe+R_R)XnnFi|mDUZo2$&X@}P!nlwh&=Geu;4u*vE?*&ZO$XU*NA3DDg9$`Dq}K^Fe#-W}g3RIcl;rn17XS=c8{V`6*+}`Re7`IWjKH(j0{>DKdj`~|B%hmc$d*QRkB!-8%)iG)Y@-Gu92Aov+_-173-w&>1FoGOrPmJs&mq?1sZ0MM&!h&(kIx+xHpdy()V0QvH#v}`UaC=FdQ&8PEMA65X9)2i(jK)kB7E=pRlzSUI@X(cU%WVYDDosU>83K@YaHn*Eu#d@#it@DApVf!DQ+qxhXA_sPXJhGd^12sVySG>hym4M3WG5VDhIz7q=pj-m!+=_@1cj6G$2(!*yA968tz?Z;M-n8bhVu0qIhS5tl|*RYPL@~-M2<qe9l@6fdo!V&A}bR{JXnP|G7Pe8gRG_MFiRD>0T(vy56mv(e<_eDn^IG`Nes5+)(1Z@twE`)5!avsdOnHIQ<!Tl(U~wxhxYgG62lRVDLiI-kXg~DC4_Jz*GgP%-2<Bh~9!6hu{hp2<U6}v7JP=L&Z}UGErh_F`IJ$uljO466aOc%W05oNv7<|Y0m}>S*)(OQ!VjXvKUeAH(b5(f_MfEakK_-0d6t8jg1k5a}OM8r~Q*G6;T#h->YBzT8r$ihKNGYn;>6V883tSo}8x(|Fua&+GqyOi$4k-B|aac1pX(DB}t5fz>xu$-T4;dI%VMvdN2-uI;;k|;8rq7X_*6ljR`WlW-2kX3(xq>`9^^hc(pEhMdeY(6AnBy@KJo~F>>b{k}<fr*)uyBIH`KyS<EFm(fbSb;(4~0LEH|&(b`<1lv|ps5Eh0oaVY2zjyF|<&<XrOxpunRwGja=#1^w46BxGM)>9*d+QM4L>HPAcj!vl!UYubj6@)_@HjLFx6fAHCC<{2t1|>#Nq8FC}=OSgcSKn*7P9yILs6us}AX_Y~bk*|?jHe)}CvlUClFq_+&Pyjlm61?#w~ojsv77j;zzCTZqg%|^>i|W4cX#)0Z-sjFl|Qe`<K3OUIGNlsrA<SbxhIP(z&SFjaSkFV@Idx(S_f(*MotwMusp$ptk|n$EZL&+Jn_zhIHkn*q4}%3;1f^)GpAEJ!83%b|M(^^KLa7<xb@bqm&b#Ljso*(hJ8NU9)Ke(H(F;Q6Ea6y!~pLI_^mdVgq1YN4_3CK^kdl!u`#hY!Eo1{JF19M5!(`6SC}{&27H{SWVOqYXWWlWVuh6^l3?osNwlZivv_S4Rse{bJIOF8&p&PkY%)aM1h=l3l8$%}Gw{RfH-CPpXTmWL>8Oly24_C3LkZ*c=)er6^66<$ywHInUN613dfi-PcsIWME7!L<c`CQrW#J8ET;#UxKJ(O!y=f873o!3*f!z-?d(0dquTU<w2%2AiXGBBsjrImi!1bsHM!CajRH5E=K2Rv>fYrRrH3Jxv3MrsK2U_mvh_=*vYYI=fCKFkSAk;rID{^me6yMsZ-_>x$jSwYCu|R+BiY({dmgjm_(77T?g~uH?L6zbSBJCha6*<c{%TBl?RLA94&GrbK_^cG!Y#vOPm!aDMvSZI18}AQXl$+k{c29?_8+oIFvH*5H&n0j2BceEia!3N{53tlU*VzreiJSh;w+wwjc^E-vh_VqFOv^t|R(%FhM%}-Dh>O8mTbfgt23dCY0?b;T;1TB5i^6A$`6{*h*$`s|jU9uH4J<N=bx)gGb({op;&R!u6-QQ31`N)`o|(IV1tFnB1`#40Tw0TGGTi8@Cpq3ms&ey%r7B!R$_Wo@or}sKr;9xInGHh!;$kyKN+K$aMCM%*8b|ycP#mx#hLupLVfklW!;M``R=6Oj?nJsHt}3V+IbDCHo4ah#Da>^M%udX8{PJ{0#*bfa5>+ioB73eN6ca3VaQcFW53CR)VuJ{R?)n_rEr|7tCZyQv`_x@i1oX9J-?&>8Z7T{L{3Ea{<!voNUe*TG($&id*dDJ<O$0><<185!i|4(&U}pn357L&fQwpSX$g6NYg5b33&Rk5#>&%L>PiP(!%0@AA;2eX|8?p-f1X1Au{PH<(H14=$){Dz`-@^e^c;=Ir6eQCH&pNd7;u>)>L=l9K-jB->r9cAzschptYlkg>`8X^GlT#rcnxovOdkCor#ZSCm9OEk{7Bf*X7If8#G`G%V!nk&|iO_nWodl8!bbChO=;3A&38(nrA$3#Msk<^hTIpgmGE(*|HjE*Ycftp2ZoQ13bRa#0%IyW^zV~8t2&uw-zo~u5oOfLO$P^%bUBNSBbWPvuoWFIGcEzd~cbOnwbR+iWHwGX>oqJnkZhQpM{VC>Mcxe>{KM_l&k8L^cJh+Fy)}b=^2%@f^`Z5}NVzb6?n5T5FV!ut_*JryL<t;*=j8g?YqXCwc7nh9G{_6_0C&o9lVo!1+Wbxf)_6If(LUxNSGY$At704|v{?RDmUZu8Lc7^6XOJpyuDTSC_)K22#V|HNN!(7~vMMPv4WN<T!_kYeZ^4xa9x+^#?!gD#qndc=Ij!*Xm5>LRE+`3+D>4A4$KWx2TYE4E@+``bQO~49KpNrY75;e@K_Y=zmwGHO0DnY0iqmv3cCh{<hP$iA#9{yLiSpjJsLFD=il_fGUlEE#XK;=u73YO0?Sbg}G{m7*Q<SWZr2Wtt$8H|6ou73e6d<xx1ygN%gV|jz|9+tO!u>e7O?!7ubf3Xlu>qCsekl_}hc}(dJ5JZ!$Brww^fgTOkZyHNEmNY_kk!He2s4Wp@=gsIyXm8AVvT0S{bfoFo_2y8MHeJcFBr_1d(H$8GwUcOWo)3Xh;l@1(ihLxKd@?hJ??j<ZYsa9+K3!X$$%P|GT%KWW@(Cy)tcYB3n6M!Bv%?C@OG4snAQ8H}Aj*MgjmYh1*z$Li91$=KVPK8UFEsfzAl3v=1R)@cy<&&pfz*T8KC#d>;u4ryrPU$j5l7TDvc`<;3G{Qx$C`(S7RIV_TT1?u6tP_NSrG0qz&~jQ*R+$sBf-mu7`{W`TNgU#dQik+MesF=$TJ!Me^OJH8>`DMp8j&rkzHgc`2;`QG>4pCrcXf};Gc=_pX?1Xw(4%p{5gSwga~Rl{6#b1{tn<RHmEhudFzTymcq|luPjKpupt(L2W7Fq#%pW62`vB5DnY7+HOL}y8!Hh+_hQhpjo#deW(Nu5WLc4lSws1pLhnk$&T<5{TB2gkag4G$TY5{`>AYpIwep{)>eIe9tbR>B&2;S=6nUL520kiwC_KgxUsa5cp&Ng}sb8qsB0~pclQ<NWqPVEwhWa(s497IQB3FP6)+DA*6Ohj@;Qdx|ooq*ItbxjnN(2<*<&*inT?tK9+<f(@pFM4G8*U_`l0Ld?2G;;`O3&ZZH?uVoJL*E&Wv`hX?$sKzJa3ttj!U)Jw!z|Bwn4tA>~D$`p~BRt2NK3+UNc74D7H{Vrk+4@2ZJ#n(v+^41f>^+)`Tz42-@5x>G#roXB<)Bs`;9=+QQq!K{}{k%sa8r+N?v|+12}I(fcJ-94;GLy;JC}BTm8sZ3=x?**N^3?OG0fZs?X}CTU@6P4D9PEFt0!<v#J@6?Po_=qiZ@u_&*=;Pvh2us4i~xie~?8%8!85ZkG(7SH`9T^SQxR^el{V2En40{cg23M*~pHj>oSvKUGLfrQV6l+>eQ=b$0<vd%dIn1QasP|8sb4=&%q3AdJ=BaETva*?u{BHhc*!!f|gQ$`_@So}((l9`qIJ<RS?<8Y))L-q4hkT)vU)+<SE7yZbo$~H-G%b*?;UFf)n?Zb2UYN0sTfA<}r%P=TGPs!6kL~8fg+${e?3c?;_F3LG-K8nCj?u8}rgP0j?Iu*_pZ{g|#1T0kqyJx#Ye7g@_n+P=lp0V#Xnkp6iWv#lQ85^y_uTs2SA)z&zl{vBi7IaMz1gRy%+Na<ef@*qOr;@cjBw5uBqF0C{u+ELra_YsNS0_S!-UQJm3L_h^Nts33)jr2C@QQ3FYT@8AM?-5^g-m%Hgiyz=4P~s({C5B}Fhhl7Nr;Gq%v|ZluU}-Z6WS?L<|=PeLEnni=`vPf0LN_SKo$TJJtsy&3ercLb`eO)EOF1ORi}hyb{ufR4rZHSme+JeSxK5};D)wkUhYY%)OJ*LQL*v%jS(34X*oi;?;>6$<Zw435`ec=PzI{J^_V5rz)jndMLG5%pQ^T*OB<ZbIGiX_P#hoCsfl9i=iPj#7YAv>gX0;iyC3i}vKn2Uk*O6V^1|GKEajZZs!F>Mct+iH_(O=!i{G`f4t^+LOH_;3yZP-9XoLFc0a6fqExZ1nCChID;eZ&1!({5v6~ZI!?Y0r3LmN;?jK&lNHbETXthK1NCh}-M6(phi60E%~xCnW6Wy%iK(>#_III}nMN<3Z<D&r`6Q7I_!xZMRV6r3g@M^I32;-FxUbWx5t7ZnJGS^D_+ISH}Ts9Z0hX$%0@@dxG6!a5-nYB9yyOe-HI6rp$F2piFInlRs$!;!w!E%zzerSrN_=O@w;`<14K#9d`c61K;nO!?_}9o$kn=a%jET!f<{ZzVRjYy9f5^saQrr@k-Q-dpU^vg-ofp5>e5Y%m0~!c2m|2U8rOb&;H5Na31IKiPqjBsQ;;)LRc(FEnCb*o!6!=)kHmm3OvukTuI=F(?h}nTHDZw%~a;nC()-xTVs=Vd$`eW)-{1Df+gy@bgmNeH<3UJ-hi5w3~(qPGUFItHzKRB@5wsS0C5Zz_BP=K%IT?>$+5ID`?=ZjaZI1Q%vV$OOabK{S<z`!a=(Xr1&Z;kuF1R5eV2+1gN2{JhNWDG}k2-Nz(?LYNJV;!eKQZbp$hW=9D;M@z@AjVbkJSj6blrdpeOcPSKU-V0oP{(L~1&A~MLUVk9T7^J5!lzf{k0z><$YXZY1#n1dtQs44W4--Z*ASuJeTV>xaQ%zBJKVkIt++_Fvhe&Fm;M+JYA>5Egq@&(4mJ1HoNi{TeC<Ml`gK8!i-*xuzqLD{7d999~!$wy{E$AaOpf@ZGZ^4^sg6h0HD=rR+JIa9jsJRCQ>c3(q_?pR37Uzi(dG+6{qd!vAf1OAFEs}l1U1uIAhenG>72y`e?6j++n945RKmvoWJTLJdNL~EF-M^pbV?_M&F&W-hYoC!zBy(p4zfF?!2pDBB8<qV)lt3jS;n^SQDC&hNi8In<@f(TlnD%=(Y4p=_nF+@S!Q?oI;p268=wzN3L;eB)pfkRzY&&@7ceF-u_St*wW?nicwO+=K6N=>5nZXX}p5LfE1_jw1eEP{3U*)!q?1~JhFHmaQ$lWLo`<ue><S$npy{LZun6qJC#Dn4dpiArjX+42mp7oiCFGDy)YFSgGbdpynhn3<(3Auq`>;Nw*=wzJEOzjM^B!qv4wyIOe9JuX5<>n1^KsZ9iyr%_wI!+uaDKzq?Jy9rA{z-5yK14BD!KM=A4&PV_kl0i9sv&bQ#40|jU33-m0Ly*fY|4g=kN<spkjpX!&XLQ}k>`9nh`YfI#Wmc39dkys8H^<M1Rbb>`N$&+<<m`!U3$Nk8<IQ$*N>!vRI-`}z4F4rTRpCwQ>fm7yRptbtrr*ON$jQ*>LHZo;z<m@6vIqhmp|tE^XKQR5cmOn&RE$<bDJT}-W{QubX*=^Vuj<$?L-wnU^=&;_8>2~G*O0YdbGVyiVs>-viei#U*%EfB;Onrj3r5DcH?}8_=SnM~9iId2FcpV_u^hZ+Q*B!;c`7DX;vi4tSOX03lBLG5@~K{RE}aX$@dgcdm@1C84lkC?ZKDl<@G)IyC!!r&<ba_Seo%FMY{orb&k)B776X6ttOheEJ({MO$z@}pUSj8`g66}ORz17`(DDo)w`%aHsq0hS#B@K9wzO6D<`O|-l}h6Ki>gxqzTbIDL*Bqm6J!A6y3w2GP2zw++b_|^EvObrL?l+<IWBMP(?fZC_a0=fp53k=&mMABS2WJ497O&ju)4ufCL(KWv(c-R6dlZAg7Z|gj$A+F938l^LIUjVMU(y@vwm2lf_~mSIsr+GznF<}2JdaQCx2YYMH!`x&?AX{h%|y-cU&E$TqR3cEJ$Y8lpk_QuRO*bvw335^#^gWc3*;mRhHCU%S7z-7r|1hUsPC5TF3kv+y&Kn;mn9DkFN@i3Q9UV119iM0Jxi~whB3SO*dtVKtQKGS`Rk5s`rklvF4Jhq@3C!J=)Skm;7l|HxUsOxX;07VMyf{n0@N}Ua{{cD*goMn?^HZW=F#LQZlJ!+Sv7cCGRw#jG4}iwzsZh9r<iVb=sFa8e0}vnOPNBZ>ogDVsGZmx`Ow_VV$JA?|~2sF&bgE=!=Ht17I-&V`YBh?m4T0k6A7GMI5>vC6k?bv$GY==u8EG5dwYDbeEzMGmLbzSW(pZEPLAHP0$rF7ub<@W~F{<uv=uz<X45>y84tQ?vjD&F;5Z6k#M97(lG9Ya_|xnKV@NE!uldMP~IWpJBH>Efr`{Q?X0<7l=U!b!>X0y)PdA562C0%hZ38CIP26uDW3bFA9Tblt!04#9y<Ru1O5ceIqVIaCD4>RX9r!b^V<rF;1z<tu<P};O$o|BM7H7z@hM|JicZzA$v#-#mnyTZeJuHBjyd*$T5(u$SA6}yWLLAi2)Eexv+&+T9HyCJ)78>)!gg4qyHc|qw>cRp$Pc&?PiSvuJ7_Rnt&_9X@TJJ3p|Na|@>Ot4O;~k2E1M(%#f?KVoR_rJPT!-f#OGe=&WGr%)SJKQszf$%v){NTZ>{&t$FlV%A}!6aCuxBqaZSw4hpCjd&jztZnIdH)3=Emyri~F{jD5r$(5>$$Rn@J5idwM8`Vp<gwlnjhzR0#*S@?ZQo?7dW22b8Tu0eozP>mTKPoStbpzn*?+tQ%(xVnyS0SiB5bwlARx7D`s1XNy3I3d@Cmpf(^Q)OgA2<9}0Sgs_!%qDkpQ;zEJy};|j?`Xj}ZlEzOGT2(oj7zEke;RW+n7NTE=`z8;E?FNe8j^>3H;>+aHS4)#Fahv)h!ynoch(~<2ZlJj+_l_hY@bGl`(?Pf?v*AJsDi|w-6TauosRbhs_tW@&K4czOJYSvc86n+w$#Sf7RUUDGaa;P?kpMEAunyDrl_j(11)Qme7xek<!%eT=C%HEmKK@J8k@_kScsUVALA;{cvb2jE%|GU(^j(X`$89xV#i8UtKZNx(2_825a(k(_+Iy*0oWs{uoc9+HZQ~x)o>fexm*Q_V^X6V6+@aWhZb=~&y<K+T9w)lg)DC}$bou@>62P=Vk&QQ4e6NaMMgY?xRJ8uU;P;O!n?H5%{B6n<~eJpo%Xa1OME-bzV)fe%7(9s>y75&nmoa^T*9CC*A%)sd<MM5p-H1J0BC|-ns28ISR;ce4U@8(wKjb%0?bowv`2l{X%`&V)$({$2UzC;QA*!tU?aM2U2pfi_q21jfn{|&jOQHRm+kpJ1!b`V;_UQqUZQrC`Liu2$UuYaIwrBI1qZ(0y_rUzBQhh|jcllYd)H8fcI_sna9Js%Qs5^<=t4dZqXh1s(?=m39{<h9whlodY%vEaq}LKf)NC8>dPf=8wGK6uJ6amx6h@%Xq|}VhEA%GE?wf?hl<~kdf{r}#s#%k^P0MsBbRepc%0$P76B#ph6La13Kw7wvp@P<<U8fm>ffFy60){k0V@9nglQM$Ze=J+xO?po;aSM<Uxtq3v1gwTCSSMn*J5bjT=I+Q%P9(3=l01RfFN<E-vQTTT4P~VuDO)NT@vF*b5iB3FSjI_j2e&_>l0|V;F36Hfr6gwX1^W_^*#!UQeFV0o`(%5gmMP9*Dm59DdCx&Dj0e@^N4#G%%WWX|wbEbB;I*+=f-Wf2BPwSdJ0;AdX`Cq)L#WX))`*x8#^thXlYwXVU(OcQiVCzFhK`Q=H@CLgi2YM`jov+~L~MixbmaOR`=bkDKHqQp?lk1gpmaFU^9ap4QMzSET!GN!9OV2iT;_t^-p$gH`P8Q&2^nY%1-&=v(&{RBJVTVOiIhKs=)hosuv3<s#?}E8DAYQj*V$ZX2nvy)#g003USMJaYE<-Xwg^!LncbW>s3yY#pf8m{c);HADNpXQC-4KB{Me|k*zd;4Wj7)vaL1Q?KXngkLi-+Qjq1#Ad{BPXDDMh8!|h5P!dCn7nEEKECDy!RQ$y(n7uxpEa%5>8XMb6>Ythy?yJSA(<e5Wz&3+o{vYf4&l-3eQ7;4alAq<Y-(2c6D=}k_L(-k>7EV>WaZr-BlSie71{*F;q5^|+wLM6YwGbowZm|=zvCq2gKM(Q^pa6OifWIpQv6$gWP+;I>@yG2K6D9byPA@{|~im1}s<=PXA`F2SESV&RdKxk(;N<WsZ(3qgiZrm>AD`VQML6afUjh&NceY|M<&Sa8QGz@GMZbrz*NO})L1AD#)prKML8VCOLeX6GN&u~pA((yqi$!fh$oUcS7qvV7p8N(~r;*_95zHaHKEKMTCygY}GTEEJ+bd6d=RXa_IJh@{t0;W{HsI0y4Jj-yO=H__F0VPga=6iI{Bvq)S>!j2|&a)XEARB?VmNpn>CUj=+u`LXG;Gv;(f4;H4rCk$y)mA9XUTX&h7(;infv)QL{p|B)$VEjl-V&B5!e4&IO9j9LY3u_7EkJvscn9AHMUjoNM&V}0%Cgi-FgFYzYtJM=I_8K#p%CQ&*>xr5WVYBC8@#r4xUtF3i*Ny<9gz;C7-RLxwiGu3{iI$<K98s{IC;W~T~z4L%<!fQ!=OoqL^odmSQ=KZsV@llkKeRx(717)T#dmVLTuaW@eSu%aI}j4bp(!5@+1nCFbPV#A(o$WCuR1AE0Zo;i$l(3B^fO|Fq7Q`#$CT6R!Jb@q)zko7_rp3ZIsHukUk5iEVoE^x|6j!1W^hGuSBCiDMARo(MZWDjOA)VnsV6B5;ahV4tpmTfubaDYx(^2R6CJ2cd&u9e3}-%ADPOOV*#*AO#Rji9XNUC#LBBe@p>@Lk$}9RH4I+-u3&*uudWC+jdpQpFCS4Zp^ICn%1Yf7F=qp;D2_L9KS5@@LJ^IM`Q}^{%}Ul_Agd5X&nUIRViF$J#tsmjc3D!tsv1n9NDyWd)Hx`}W8aAaR1QrMgd@~qt?U_nk+PkvxRR|ex6xanWW&IlVi#n*kcpn|k`UEst(M&eeG0l(%tCwny*ch%&-HC2;ob?2$_S58pNjwJ^s$sT{=Z=EQG2Qt0jXG2KAi$K`KhI(+q}gZcFoS2P!;vu77f=TfKY0xhBz%9%c?#OH6V@?eUm~v--bwH*9N8)DT*uOay3-psn$RqN--itmI6TN_kh|;i{rO(a-IPG?T&<wS#uv8*KkY3wY6w25*T4rjbCurS9z9D4msi31YS73x<B`Zn35`nL=h>q?J`*|C9f-*HEFjlUNB*3Y$Z!37F}ux%3y{tpsWJ5=$ah)=qhC`?8iK9VH4iq`Z-3<C1bi#Y&S)Jgycu5W-oxpja+WBo>2DzyWo^ij8n(Hv7NX@E4gfqT}T84&PGdQ+#89SolR|j&Z=#?!g{FE@9d<}Mtdp4jx&g<3e+mCCFp^O7GqGrm|rO>SgYbIg`2(w@S;h~tw2hxRiYbg!9SF=O&nwMF`d(7?S|BBsy*7RStqC%X_Qykv7<_(VH!0CE;M@!4KFqmw-pA}@Hmi+?`}0Y=CP$#Zd6n7s9i?ZF9u;)WBHV40BZ1rXSe1FFGtU*n)ZX~TgMavC5sx?>glLmP&RDLV~WP&mW^=HoF_2j?Wwnl7jSM8Yq7`r*p4zarzNvNxkK!j(ngmx6)Ww}nq$K9@wzXx0xvY&;&6eOG;3lLpI*nbCa0CJEib{P$t?F)JM427qtm_4GY6mb$`eqz;0#C|1}hNZ{2OGbvc`H4lhVcXC(5vup1?8&g>VJq0vo+vHfmD9Utv#yt}9FhL<m5lAhANy%uM*f?n}5HRpg0alqc8{#S}&#^S+Mme$_uS%=!&94bh<qE6(ZcvIPN&_{;#`C8pp<t7}x}^Q8ePzoVNemD?pkt{{YSh(`x!E6<pAfqitT+1;RvTddjoSgNf=oD!8+RY08b9j9cSQclsqq4DIo9NIQBP$bHiiXKaD$9P!#5#d0g?rhWlEsz7C0h0J@Dh#J+uAngiZ?#PWMQ63bg@E}eo#yeXYAqM4!%;D9zZ_4@0>)F-ps0Mn)`iC4rRKBmZ;pb-pmJoS1szept&1-d!1oX@)6+Lmgbvspg^~+qc~Pu5T538JRzLKZQ-@KseMSP`jdtWt40DMG4r{=uH43Tfx<gfhkRC1YKz(%DuXOcKwKL41AwdcZ>9OL-0u!Fj!I5ko_*TqWn503jwr`Nnvgo_nX{NkJG-{7K8smrq0nc&XmUfIyqnv(-UCzQgI&o7p0k_L6w`qEiO<}x&1P6kv*dk6|G>B@$)@KYN>DK0u91=foQw)845I5^2`Gxeu9soCXH~*mE2FvnC`8M}&$@5v|P)2N(;YZmMczXWKDVB1t@28*w?PszxxVaaYk@}#nl;V`&+mLz;U~b;2&TYRB^;<Ezso5CA!752HR<M4?J<*Ynxj2MzJyA9oD&IQ4`<7vDZ56?v^^XIZA#kXnVxeWQ5NuymQvqIkDbgyM#I^)F2%_DQ{a9cv&I0Qy9;7vlsoACWHWHR(MfRlii&(twiCZs6fO08f&M3AssG_F5okU%+QV)kx16s)CR_B|^Ce78xx?q_O5sO5wpw^=c9{pOQVZ%UPhH-FE-(GOF!HRSWn6C4Qq4{@tjwtLS3CZm=f9X67VEQgnb+l7+oWQab8hHYXMDO^~>4&uD%SL#kfH|H*KmGk!=9b&@TnT2ii@V<%CI5m?EPcti6;f&;Q9mPHSFK87ECR=|Tr@2Md6o>k*WpM#wqWNgZ^k#V^V=L9XuBfeUMI6IS??4M<9)Z&gPK5J{}cCUPCn_H&UoDl3deK-Vq*kAf7u;RYo8Qn7pHBAt}$b2p`I)s)gDA|XOy<dmDyJNBxf$7US1Y7ROu#n7p<$}iEV}Z%;*w#U<on?kq)90#d5PPN9JHw@FN)?63t|&nj0`7Se255X)`hfc<`LYqpG2#EV*(HrTM{&v~<_DRS?HG6>8*V>ROg_Tbt}=e{yQJYu!LrMJP05ise)EvVlr!b*=*<bEXl~1QVPx-k4XemUP0&3;FEn)2A^L+Fir!C|~s-{}<5C(+v')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
