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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rM%O^;kha{MoIo&%?QNRhr#WUoXlr4h*CHr4_m2=E#PjP*hG&G3IWH6PutUq(hmW>u5=00d~zGwfHdDyu3pGBWbV|GoJ4pMUx1KYqFRmme>Fc=`VQ#mCEw|M>a8{_Vd%eemhWfByW-fBxftKK=aT#n&JH{?p6v-+cG-?ZxHAtDF7B<<-Z_`;UKkck}wgtJ_bX@4wx>{Ph2)kH0zmgZJO=c0VlsN#PeC|L^i-ly6@B^}`Q~F(l)CzkB=kIHJ4n|Mtzh-G%redCmLZuZHsVhc|Cu|MY3vZa>`p>%&MEqg=ip|M2)Q{C9V&!{2c|Rc~Lu+M${H@#6cNcemf(y)gP|zk7eX{7B9$w1Rx;9{yl^GNi*p*H6EUGo6gg8^)`b>(z>1|2TEa6*vy(VW*H$yx;9!fBNU&?cUyee{s3-=jh?(m!<@U^6(01((ZrIBU(N8FTei!<hk(~ahl-7eSdp+&dE4dPu#s+zv=s%55W}IHjL+E|MGVCj=Xg?+mFwIJ7e`Kg&kr%InMWS1@B*G`II=6$4~CRzrNm&bA4)P>HDr8cRI@E<VRCKekXmNY3helMm~43uAgJ><J!k(gvZ-6e|kJ`^y%l#`r7u()4p~uxW%WYS2i>D+<cPLshIG5Xm0I^HXeAmuZ}0|;UoF#GoK%S7(Yfzk2}NUf;nA$6lXX1adW0me($TBw{Lf^Zh!jA?%nO1w{QOS?%yTObLJo?4(8%3eLs^7m0rvAiw?)%YDkIu6%HvrNuIx@Z(8`2rP;_Yef{p{hs+H5w=>II`RAMD0S}%V-b1DNH*TkgH(mUI-cQ}ZhW`cLK7P3HzU6BlynZnh)7tN6z5JqaM&l_Gzgo@~aE0#|h<r<Qykd+&!rZ1w#iu^J&B-|(7Qgf!$1gg3x7@;OpAW6jVOpZet;h6m5zueBA6)6pz|E;|FyqZuKQ!OW{}%sN{quZD#Up6KY4hENqALM{OoB5dSEui26x|7MiXMI_cmokiNnRxT`0*G%+_8FMnFn%k5JtQ<;~+Pm2qFvl)zR&+0EotohoWE-*Fz6ujaVB;XoQ`QL!0uZV0(G5st3;lXn)Yu^E!OZw=duQtut``?T0TysORC4sk`_7_T9_<*SmM`{_d^!@+Cl=8Zn^71Dc}%?+@@|FqYM17kz^W7(YJZVBpNDUOnMBZ#?8b`hDw#H5{eoT#M%%4!XFYbpSTb-r?)xixIz~iJW9#eU^u@XH+0C9o-*S4Xj_~0I9vipWE$Q5A~~$zjsIQ_|a$d1XscQZ^IM3GToe<8bHu1<tcjW3+_4(xYF0Ye$wGyW0xtojfQ+mFb)>O1Z!@-;^C{0%Xm0ZCA>ih8^}J7qhDUO5{e<T3t(~w>j>9IGpb!>1eRC030z*SfJ^G-DIW%9RD(knS8mAJWs@;D%^*z&zIyWeps*p$=~bQC<5$8MVdbO^c(W&8kNy@xmcsw5&SdgjwrLtz9Qe9u^BVZf!PpV^uYjliHr>h@{w095b0QoY`}1@9nV-kw<X0b?jIQ$;XJqYe4m+Oi#7Z`wGuIX}iLQ<Sz)bUn38D#n@_02nt|&O5BC4poUj&4qROejybFl*-&tu>-7jPo7?U`3zN@cLupqL(GD;C^(@Qf2|G*2_Sxmpi0M2ULfMw8^}5QrHO#yCTVJx1NlaqpWszY$(TXn89fOWY_Hh#qD{C!xVR9fnH)N}AlNdc_3)1SiHg)a$rlEWViI<Q?Z(N4YI<a<zQZzrPR+^&W6IXU^ddhhyOLI>qPAx>JBtI%_u3Y?#iMqpn{Remw^e3(9e(<mq{t4+CP4H?}`(YzIc_8{Q4tO9hm%25F9+SKwBe>;|KI92B30qZ**O`o1IeE$Mw$d_-Jc>JCSeOC&4~_^J86+9VsA<~Z3p>+w0W4~N+wok2Y1w~C)=?r=U)^bLYQOafL{Juru5U_?tShuA7HILf}aM&@y76)UFeG~UoETcOfPt++V`Dj>oLCNqfDvc;c++OoXI6n~fj+x1;?4oukhjBzp~t_=5*m<L&aP63VNB<JX(nT&Q<7*O;jkD*)UM1kkvW6&DV(IRecKK<|6<L&n;kbZqp^Er>+-D$#cx!WmIVSOez<4nX7Agc36_?=&1bDR)x1IGnHsMWj@q;2J;z!iKLNiEV#5VSn*`@&WzS2wyMIinNHUQC%leO2dCAxK&r&Izyz%u-3{w)8A#*c~ZRlhbr*WW?78;~;=NWMtrwmT4v6BZHI^p9U?3BaI9UJsME7MB@}}V~~b*EJud^(*AvL-D}Pe3g19w2AD0m#JZexG)V*AXO#`X2cnwX<Ey1pQ7%$Fi!TtJNtHlSug>cgAbM3Q8|IX^c;fP0723qR<j#=GJ=Zo_zV~Qfss0jn>&*+%PI8jqI^mHa)u7}L`OX5-dn;p#D15w(Nm1nJfQAf!@j`OaG#*<4V;u`F66T=e0--XEVm*3k^rR%;lKpYyT%gtT&>xK|#k}bGq)8^GO8YreP)P<hO^@7{C@Pi!4+vw&%QX+JJb-5gQw~H}$*>r2t?9)10f$Q1rgJ7=D?PnCYAGO*cHEiBC^9PMjPmSd5Q-<qCh@StWK{Eqth%oWLwN)9QfQR73>Kf}Fx&}3iQ}Y%W0=Fh@*Dsy1c1_sb@SJ6R(3_Jb(u2~b|;PvxN|I5vga0Brblxgg}0V41+#idrFrvBA9wH%s8mzXMU)03A;x0{#p(OG@&b(6vL+Q4wK<%;BuWg+n?x%#m7dHvsuHLJj}qZubhsS?#Zc)|R>R~xiS4ZdpY!uEN1OF@@`8DK_QZBX+q`hasnzDd;&*S}{&kUi3ZBI?6~$cBC}t}l33W7ARQ2@O8FM9xtLXdKEXZX}y+J}$(G>{ykMMFz1!OlH%-DCxnG|XaZfBoJ2?xwL&5AY3*=Ko5!`WqUuyNTBV~J!4STaPb)qHO7r6t!AjUi>^ZH=7p5i}#Ec9Y8QzPY)1zZ;>RgCK&`=~NcP8YfEt#NdvP!k*clI1vc;4sV5W-UvHQdJLFUg7KyTvO<;QgNOwDz(fPCaLiKCdRF@P-C1Px;rn#dtDA7p$C*MGRgF>7omX`L9NqPYdv9sWNOh3N^yfvN6S^{hdjjr1;uFx+=d@b{5q*`?HnSb?)L8s|Z^jYbfuw<q#PRX3k*4Fk1KA9*rA1_wK<7GoSLX+F8{*LBb%sD!FWKbioPfszN!*DveC0CU5vmQUHVf|q{%A~+r_yEuXNu=g*gtQ$&w1?7edgT3emrf3(U)$DQ*h!VbBc%6X?W=c#D?J4J@xiFNgx936DiCBNQ5wJ2nG1M$&sg-r49j8Qv0vlnkFjlj)*0zYV7C$y5V5-vSS>c(q~j|Z`uq4PzFX?i36Q;aDWdvFx!leINsw0Ifs%m(LgCuO5-%oeeLH&iYd4aDIOsfZGgW8oSQ^uCZ>~|A<s&Kg5#U&`uI%zp&3Q_mAKrfPYGCCeWW*N1xArFBb>$)+(}bd8OFHCCsE;wNvfMS0f$s=`5_~XsuMKjAq^4jqQZ2>;l$Ns+C=eplljDuj=o-Haw*5cWK+?t)NkwX(#K4%S~wq4EY}G*!7I7jh3Dmo;PweSF_z{WF0`J^WLxyZO$`t5o_d)#)e>sZ1x-V+CzON4W>1Uj(Odv2P6z5AorYHXYLfr?*`t1{(}zMx<+FRo8@#7*7xmx(yl9EnrC7x^S2J>c-I8JCc#9byYzp+bA<+<8OUI66a36CIp@Rm!(5?)Ge4?2|h4#c@rNS&dL4+8GfN<9!b3~LU{uVO=?t4Ezt06wJa{cioq{mCI%RHQ(!@7x8c7>!5y1+u9!56Vpy+P2RTsah{1#ys^%Aqp*xw<=*giXa@2?ys!lg({{bt&ALE;QdDrvTFJ&37+vZ;BO@3O<S}3C<%}J?G)rtTRjC2>FW5Cl6IF<~~1>Z5rD+MTC%?I6H+DEyPa>ihqR0wA>gE)8I)Sf}4csVyRNlLe^jL+?y}tSNiDdLNx(fg?%uVA)F<iwT#OE?{d;gtebiTR-UW@aP<lp0p)3oQAs%04gPlbUgzeU$hqucBNgtFBZpQ8j0658exgk`0r-1rKun}nLkEn|f)*M2?o`Sn_k&9Q@$#k7U>7PK%h|C=Ijm|rWkoa!YFXd!oF%C0$pCazY1vxEOJ1BEFVUXQbs0LLkOKTI2|<cg?p~ZhY7`vL&8=Oo%u%!Nn+itZofuQ*llpEnRlTFju<%6j`Ac87jZ)cV?UD;bZ*SQ|Ai_PwKEbU;B*YCkN?fl%%sp5mI8JH1=oE^Q3kojPrWI0}-f~Qa0;y=N;!iEp4yt5aRV&{K-eN=ofn{=BkCW)Lw;96zHp&ra{AVU$<u&fcGdm_!RXCHXOF)HAMv2HAoUk#z(<=itT@oh3a!6Td$*78(WL_ovp?Qi}nO=yrH68e#mRzgwhN2QY5t9ylLJiIyH2Yeb2dg5*7h|ER5#l&mrBOVq7Qchh&1T$n><|SGP_YDPig5y`7v~0-s}KAmCKp!`*k`ktvRW<&?+9Im`_!1Xc;x^O3|1tK^=*q&MpY}cg4;P||4$;_jfn6W2Y7BBg=FT#{E5lo7qETpy}zW^J3g527<KpCWSg99DAMrLxF&+rtlYp*P=3O(ZJvgw^XfMwRwId7>$y<=$Z9<+uToc~0O>FFPnJf7{<#7t823BcvY#*0?(mfEXTUp-{1l8@&`aAfWj_%#5rERep91nRBe1$J6}%qNSPGy|37|-$gUURafo&0*qM1L!0IM~iV?H0We>?`IU2bCrLz2N>pPz!<g*<<<w$9G@MYAQo9;Tc?Od}3R4o3bd2reMueE>En<U_D&Qcz2D?KXB4%$905O|-fZFOd9m#CRxCp{$a2p)V@8l1c_F-eLl<Ad~p$c$Eu<gg={%5Q>Gw{lzw6kx)^AHz;L{1@SDO(!@6US{f$LWYu<WyP$w_x#wPoaTDEGy+xsj>bit9Joya}51v{Q032+G#%slz59|J9N&S6@*&CX2F<D#l1ZCoTxCL}7EO(6)^FU3d5drzxD?76EaT4xz*G@@LCPaxuxm-ba-kO%BW>GRIdog6B?<OrVZKgn{Pw?KTprP$)=Srgi_y@$Vp$#ydA~0E{b0N-*!YDi?0FuKWR*dv9C(F=kvP)r_1ca35kt<{@bO|lLmzT|1nKVDIes@p4@M2x!-5PI@@;96KC2ghPFe2Q2Rt~dSmlx4scw%@RhvU<_3XKn-sVK)Ft?eT8t=g)w+VAKX)p%GBHCHL;aYm*Z$<G~C@-bh5E~zU<u&LFvg5gn=$t(ELX<(<f7-&wa12#B8yKlbvwIaTg(D#J=(kPQfJYRimiupgD`sWTDLk4vuEq!g2$b-b{(zdS+R_!W)yi}5irFH;O3oTv@24xi}dLHbD=8hGji0EiEha4R`UZT9W-mK_6aaS^W;a=C>b&{+yk0fUIv%rv-0U$e<>Q(e>y2XzygF|F~#r57+qs<E!JepeWN%pK1gg_4EEN`{YgO0${)ma0v|1fhA<g09)iZ|&e;8_Tev0w&vj?5v`$Wdo+&ql6r>pw-wjHP|hM1Ooe6ca)ikJp`=X*p@YA?S+s$2>b@jkC-Jny*|5VuotGB2Q2|uvMQsU=b1nA+u@n+j%3T=6WZAqMy<=N(rin0Em9*MCQ$rFbv%dz3sk@wJ>|>lGE9))e6vJd|s2oCXyDO-(A$3kEOxwoLo0R2fR}4bsX###XHGek1MmvsO6YJsa>4nPJbp5J{a-Aa6QD<JZ2An?u6@m{nRn)`L^BlCdwp5EV!BZq>u(D?>FIM-erM^&&N-6v1@^_WwNa8nU@?v>Bv&HqO1U8DGl1>(wX^`F*^?y&~OXR1hIqFcj_JJpIJFCMNAUttY>43i8?hwU}{@R8?l_lDQOp!og5QXN(q(%xZ6|+%nqnSwP|dP)H$hA)?2{ZyxCUHE4aZCUu8S>P|3u$3fxs2>S`WARqvb*MhH(yD)H9B-2e}B=TePu3mzmvwXQ*+m+k}sx9a(am0>GZHZILfxoFw2_+5wA^u&d#v3&_*pq-L^rU!xl;mR3>c7Ae_Z!4Kw8pd{9E)(qOMgOq;-X0O8iBs>rt=HuA-A*V2W&`1v4iWi#BCZL52wcu%*1-$0PJLcqLd$k2?Vu|f?ONd;HgPK?i93)#f98~5lU8B`xAAEDr1oC`I5m#NvoFfA5WNG&7#4XGqXwa3(<D@IX?<S>(8ptZBi~lKMUnJ0K6oe!u{Mf|D+uxlQ3%22T6keUBLi(m!Ue&hP$^`XdeQ{Nv7!K*VUZC36*f`Q>~nbT++<bSX@xP?LR?qd-G?Mm;4+t?8<88KWgsvyPlt8sHasgp8;ueIq_BkyW7pTB*9)&AAs9H*shopUFf|1-gY*)pI^}-A3aD~E%unFAr8Pb;G)RH-!CLz=0UM--2FADj=p5d8;7VHBGf~QzX0m&Q(AlLe+9333>)OPAz@!7UH`*kX%K=pLob(U1ivL6_4k_D9bgQNHNOf;CVjvo`%UmB26>w;^1TN)xv!Q&aKB`x?^JU5>jFkns@x{H(UDawd>iV0>Dwb~VI3}cw!EqK+!4c`tGb`*rSA~SB>CfY%>BNhT;A@&e{gr<IUO~RlN82}uvgN?jugc%zl3XsPtS;R`h2AL9pC)MID*0hkPxK~t4oL-exwB1y(NQl+5uF~b<ZM#);cDEs3RaY}M9J5r57ms?k7yT+TrK48Iq7|+7+eDc9Q*YSi&D+C=YCrfQx%#p_P)UE4}xdBWl9`NJhs48gD_%Lp39)oYsoI%+tB=jDsE6JYyk@q!+3gja98*w!&_;b=P}S@2#eN7oFnDVd6&ao(+Uwhj|Pw?j$Z`8YIt~K5unbCCs*L`eUgP&*MatOUFmg1J&&G)G-c}wD~Wap&11xrR-zyX=`U@WfY;zJUd`Myz()jh+j=dfEYO$}5J*<POGnZDEG3(O{KQH>BB$dXAK+9D!WxLbqHPV>5byW{*S}}}z?n4~rZNb&m3O9`0;c;vCf7h|{S^qOf=3$_KHDKphwL6sWk$~|?*P`%vAIjasUPD{khrcQ{gBPGfKIunx8+QaraC)P5h|O5!}Y|S>Lle^Kcj3ZcpoOh@NaGjqUNBz_X%E9Jwq>lZ}YFRLwG2VeD=9bpY8!*i+JM?w_(uIp=5fweBzMq0|bvS?8Pu?d{~H2rLkO>+TnRM5)kmA3;-ps)+Pn<<}sLGBLp-toW)nBsER7~Yr&wbKE5RTB<-C+*1TMZ9rID<iqfAN^c;`iAgh&nCubD1Ui)t|2uJRP(#(oLxBf~=|I~DwX#v^mH{Tf23t8-Ubz)w@RO<`C`3p!3GfyU+_+w5VK%tS@>IuQOucs{$>D<9uz~8z$pI1-xTd@8R;N$}b4qOa(=HVrESr+BAL_SDqiT^_jwwOazdG?#8s(g8&kd4Fh)Ga%Icz5&q!>e1WJ);>dL@xw)5{j||1C2Z<vRa5fNVCwUthsSU;!7#riI5ANwNGd@O-GUCDOsZ*!GvEy3zH!`#h<W9n@+LD6yA%bdBU=+0$-$5_pUQDzF~9G2_0(hJ3ZLe_5zGKeX=D4$o}3eO1Sd+|4H10lIOrU6K#}1qo(6wP@%;+v(n!)Vs=C2gB$c?*rUZt3(y)(jh1M7n$e|NeTb}#a!`#}2W|t+Cm{5Ei{2j%I8Mdg>dxZWfK`R50Y@;0s*CRl6ZA~{A*`}2+wK;mQYt8Yhf4%zR7e(M3oB5s?QWeERHfx4JAqAlw;vTS>GDt1bu4XzQ$4V0gbiIHK<(0!5xNc0@E-4tft|S;`a>)T&(Kx*AYr6XNtYv}L9>!fV3nG3q}sqXI!cTf^stDXcL<KR_tY3R1*Q<|`RNL!kS|kZdl=aILpOKXo}W1Mq66;$V)5^RJGA}1bB9=Q=@;w{Lz6m0KkajHhQRfpSwgX5yTB5X?RL*io-klJh8gify*8ByV12MI0-bCHemfw@53-18M@3ar4`iT;Ne%OeN*UO_Pn)xCt1cTcx*K4Qz#;K?4D1d)hnK{dF~7F+L8223^0<W)B^D~d<%Cy&C1fK+yw;N6o}iqD+*JFUo3|Dz2)0_jbAs-_V(a3FG28;nC3sqswj7|6S>Q5hWWoW63FWRjNw_iE#(@_GO$!?|qAR14JLa--qD-PMBDiLt6X>oKOVAU3@3t;G!4WXE!<J36+7A1wg_}yTAq~mUL1`6*R$9aE4aHe5L&j36VzcPs-JfJBk|uZ!S6rM70~ACmg%(uZ9oE;aI@;5h^4Y53JsgQwLo}i<m&+P2#~(PqsmplsS_f?v5){L=FH8{HwzO=nGNRmBTl}`zKrcRvzD<omP$@BjQ@Zu2Q_KId*~xxW0YrGzE;(sb8jvb;>C=9i(hhKhBCu#FNmBf)Bx_gE-Dx$TkxBXWO*mKQw6uHTR^7XLx2fX6C{3vz+_Emrdx0>_%0;7YO?5%40-?igV>_0YCR$XYGlVG&IdKp8?b(G$j@8whR@_WCFUEzc;C{4_ODcBfCO4&&$x<WF0m7^Wc1>n(Pjo&M3Zfdo)hI#(6?}|oYu560L{><~f&z(98`ol1RcnDOjjd<2x3iwdpypajA>NB+>g~oUJL>ADmlrQ?Bw_!y$nwj$Dl+1SM#kiQLe8RgAM372tQH8V7&10ayKETmW3OU3ZxFlT$UAOOEnPjQh>58yF}V#&T_dz0LeC*qzcDv)<io{E9;y_@{J4mG`NF%Q8ZH*~vBpZy4@bJK@y9FhjtMuta3Q*|sp&CxZj7tdZ^oqQEI%|idWL*;3k3@zesS~CsvNo-_yozswB53p)huXElHX0r@1*GDz|=!{^E@{CypN)G&`Kq7P$5Ll^LY7KL-01wCxI+hhOLI1O1n;`aDqHjotW6&FQmC_;=U?hHJ%!Z<4tymzYjU4q6~7WEH*^?P8_{T^RWmg0UZYBGv!q&rQ-W)T8$)Qn@Ul<h|%YV4f0{Lgs!ij&ScOFH&pHT_WL;{L<`6wRVzVCJG#d+)#(&ipVO7qPA4v0&>rMr)}llWb4s+3H}0VQ14(ryeQSvAgWa>L-JGIZWcD3qQ*InIOlEv$X(p>JW1YqX7DKdlNR9l2J(66PM2p64w`89SK5y!}rfGDjD5K=f@K=D%32f3kT%Q*~KVC+LceLey#E>Wbg0jm+_)D~mF1d?kF)TWZ*C*qd8hvY>RAgF&N638Ty^Kb#@?OtAz7`AiBLEwVGY!o1h*_n3C28yNC!k?%wBQd{TiPn6p4B8@7f4uB7*>^#tJzMBAP^KgAMY%tkRy-yBtappB2edURIneXf96!B5fE=b95;G$eP)w)VQ=(S_ZwbkpoZox1*Zg|{e_gN>kOui$h*u)T0KwO!JN6j4^!UN)lzjz8qAHBT`k<}#nQLtZEILnjTLsBW?wHSC-mcevqGrLJI${Gn<{yOQ2y-dsWu`bYp9g|&$P*?s*F-GSG|WVnVY%CVL@_-<tHG+#B8&bqsD`WUd%C8n0A^)_IRb4+o_rq&YR28$P@KTw(p|zZJZdcF`^%eId!)Ik1*-H#iyx$cY}ml0W(4c{dT&Kle2aW^^&J9FaUz-b)-*OHcUn|t<^1W8AMCTVMb2W7NDO6Oij>l5==^py+C~krS;eK)4)|Or2LmvDEy4cd&h$#Z-qF~vcxW1XmPg3`~<hF2#BE~OJ+wRhe}}pLPUrV7%=<8>*Av<6-8r^-dBsk-`;%p^7iI*Y5v$9?{c=5DzO{XGq<$mYaQ>lM73(8SX~NVf_Hz86EXr^9X>PRPeuTvDP>yd-Vi_b1*!yl0N-<}7<;wOy&5#$2`WpF<izDIS0f@@Ve^?Js1(rwr{tm6YY{kd+C!o-1vwj!S0Qvaw8ZZDV%J#sDwRbO`Cm`ZsvhE%1*$x)RuCEvkRHuy_X#1blRps*ARC>mN&Y|-Qf*DS%aybiYztmfK{w^Kcrl39;obLIrd!p0PK_t6YOw=sqT;`Z7zRtvDt*0WojV9-qmX|nP^lU>Zhl4e0q|R7rJ_<rU=}CC0{w-sAB8Yb&^Z-5_q4+>5DCP*B$H-_AP(rBg@At!7so|>0O1^kzqNl|7pwyKB;|+k3U;QckyU@eF&_hFLvDTj0POoLrd8|-U3JjyeTUl5#KbIx5S2Vj-eGPAWE7FS?AnhAZlovSG$+(^r|$qbRGC6oMaSGAbAzHvSSjiZ|4Fy&-PQw(w!alNmG$AKD%DMO;Zg;|Vu7R|oRL1btdC`rKNVrGLQIw;6WHd_N);$baZ%^1MENyNR;<Y4({?X1t2~1#;;_O+w?}>87Wx)$>)#|7vsJZ@T71m}B(ivbrqdvd1Su)1`<O52q%0GUDU%m3=s^v)lu_nU*8wJBz04`uxnWKkfwNrD?k*MI8S+QL!Xx85O{hM8fSV}`(X;6U5QSW--?P&svfuOVJuTQ}U=aN&Nk&p)oZH&7M)w=6$E%X5Xvmfw7t^>dg}T+6Fc)LPxq@7{-H{Zxvd_;X@zEfl*Gg<vj!0!T7N!D)ohoYnVN3Mr<&-f^{R`-JLzhL?9fbKYLU-Psc~1(N1tg7-ttt9vp3qk+C!PvU(^ILiKLPH;2s65JP8=&#6kbwo5<H!~1T6$cdm9vD0;)S3{Ub!Ut<{pUrgLEIth=2hv3q9_#Y{Vci8j|?0LCdZeKx6)me@QJtG}M0LgjR!1ApZB?RkW7ZXS;cy7qKAWkFOyuCwhV5OvW`&-O$`VaHgd8pKg$_YBG5Y8>k<%i{91`p+eR4)wiknHgQtE$ZT0y{R&iY@x+n+J|Eu6qnk?3GaJP+SysDTju3Pzi?V4#5#UN7E-6mghwKl#}$jBtE6Y3q*7^?SZT>tk+c@71@@g2)iXq#%5&x2;znS@mVzn&dz6n}o|KXxHf^)8NJ|IeQn#4Aq$$Wh7~j@oc6AFY9*W;1wzkXJTnc-l1s_N;Q`ZSRFRGRJDJU5NW1OMT%d@%f;W5hl27|~9Y=ms(=Bf30yIl2k6Kp?VQQppeFsWw)7yMpm;4>xF8mYUX_o{9#n&tw`7`t@xL^s+vY((g5xEHV_Nx-nA_+@F-Um0e=JWgIDXzz1+!5f5`r><mDB>gZDD7&F!vpox+CgR?AFxypA!~4NIIe!HhKGfU1o~;S}*izoxiozCuRe*3tK2HRPDz|4vD@h)Zk&Q=4J+vxI0zOF-P`6K7M#rO-c0S$%j&@y0HBF%^c{v7P#pr!;Bysf+^eUDjmDgXx*1P6}6O+wqFzS19*FGxIXd(lCPezGIzp_xyJtIWCBD9g^3B&rIr4C|}Wpk4H@Rwq`yYzk5?W|C_;wAIz0`;*y3A~AEv5=6qp?wZDieg1s2WM?^`%fr@thSYcrz;H&!M4UN0Ephp!n@2lSTJ0i7tto@HM(2`rq63bQV|7@EK4F)lV0SMt;AM7oIKl80P+=bId~5G9K<7;OsdF~Gay^-sd|smL1}eXW{PYX7)DO9DAk_>wHr#$7DYyW`#N?WTk?bIAmzA})sxk|%Q26Jl^^YMq#<)jtbO0^9m`+`;2yKyda&f^NT5DFS*cU;e97~96snN}Ct`4+xf|eBMK(?RL>j}>IP&MeFZG;_<KX!8nzIP$thK|H%G!vM4(W;(H?#EZ)R_g}d1Hb{n|>#5o2CGE5KM|^C5PQY4NvTb-j6jXg)wpZcNSpU_}nB)blq1~Jf9Xb1hOTzRh6W~b#zDrXPD`{+C+j#8cvL9gb-vxw23_z#ETqS*cvyH&XuKQ<BFX4&TAVz5%D|QM-Ho*2OVwU7^DKP0xsIs+-uu3Pd~=6WZaybRU@pa*X`Pkrcz2gV=7Iv>mawdN=#83k>mwgX2U^$QfUvZI)gc?7LtwNoXt$;7)*@;N4jM(AUvx9b=2+3CI=2BTCwU2KHkR&1d=9hplg0y0gFd^$qU1DX%@0ojLp8MX0e{E$|$Q%=3MBkg=SB*@&=8c+5UMXVg!|i?<ICv<^98KotV^iiBe2h0~CZ%?ph8(xozM}<sfv|Zk~LBf})B(>)z?wQjv$>MkMKKQy9Dqoh6$>7(ZdJ)oX*?PBRrcOE;LIuj6Za$K{vL69&ap4O$|ITpuF7fa}|2jq+*^Zk4gbvJRer&S*N-UUDt6!5qrrb*C!WvV0_bPah6*M5S5S#l}}*;+r`}XW$G5<4YMXy(?p!ykjnHh-yXPCFhi!7~;^8?1zEDxHf+Dm_nCHbKx>-!@boR9Y^9=XnlHtp=EVdTNs|nS_W_@4?^%|2UHqp9ByY1tAhsvp<{#6Bxx6Sf6{SgnPx~>LtRS3MDJx1GdKO-C#WrXq!sbQsyOoeT=g`<Vr*s7I11W!TiJYtxSadEDKc^IfCy?Ho<7duS2Yiw2$)iEC{5UxY6hE~B*>tnDF7X>aE7m{GfXphoN~a5_!SWN`2Q4sF5L')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
