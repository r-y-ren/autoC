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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rk<(QX_`a{L!Q&%<$s<mvpzmHM>8X_pI%^585Giv@g!0pt9z_M72<w@w`P^mIi=L}t}c+J%7ymKajgRn=KlnURr^pZ@3K-+uY^?|=LC;-5ZU{B--_!^Pv~;@^My&wu@|&mVmL@$bL<`X7J$@6SJfy7=znUw^*+@!b!%?=LnNukZF3o6E<|)5kyE-@W<x`r-5E`|qdQ&;P%EeEi?d$ydL7{g;nFE&gHfkPp-Q_s6gK@__H(-A@<d2Qs$#;}73Y)8`TF)<gU5<Gc57e*Qf7hmT*rZ64WT)Q5lj<xBa8$A`Cn$EUhpvG=#HC$wOnE`GebfB62(ywOkl>BGatqg+<_-Y&!UcKCzc$v~bSwORad9L8!{2aV^?)AZ)_9j#v<9L)1#ny<nh&f!r@lUYA$gNAt6X`e1$-?oeMk4Jy_$2>O|KTPlMe!SRhdlu;F5gR<T)f-$6L{9a?-NzG?+r%$JPf$){ZHbro4IlU4;df+8hm{G|>c@w9e5*%&d3mX&TI|l-hv}X_BE4AaZ(2O~u#R{H>UoEiZl3r24RC_(v}Wsg{?*g>dVBD6DDAzny0VrQO;-BwJ2mr5{WxYQ>6JE~cl^%w@TKcpds^_-@RRY2+I;t>U4ZoC+TD5l%HxsN8gzM8SCe_^<psNSadLxoJ^VKPpyzKz6Ffe#`H38);2X&oSzr13?*04e^~2A9p6(ysy?^&Fr%Q7>XUFrDKdher=Kk)di-b2<xy9yHpRcpkC-CH5tO#*|w#q}?o?fVExzX7r{g2ioIKK9Fp7QISR~Wc%%|f*6skVsp+nQxW<3S!zu%OfJ^AN%BN51a%HO#9+$1wjs?cKEYJv%k?6Xzd_?j}DKP7i8qBk?a9Z_yeNIQr(G0c^SD5Wxe%JKwH6tja*vL1$vR{`rCzb}^j!<+pZGT>RD}nZFSPJ?4U6Mhjj(Y9myj-I4Cr+k9I7XAX;oJ8djph%}G?cz(rEm_fd`eXB8iV%@w>G(f_k!hn&xc03khN7Z-qS6c`BorQHkKDPGO*b1D%rHtLxK^|oh-o${X27^3j6YSB%ZY{W<%E1ke&%}0Sz+}(<o5v3(0zQhok#l?1XejHGqX_jW|1&nG$}#{nv*7=3Fl-{?>BFUH;0MRmi5yaKuUO9okSK7Cwlyym;w!@z2u3o;3uX$}isUkuQ@C2WRv#YjZ};C#_xFFbhPQ@xHxNbi0TTZB7LJ*n8hR3ce|!JWt_{%<9KXnQ*}`S14dB^3So~2CZLNF|{886pfY$*Ywp@GoVZ}*mrwM*QOC|kzzWU_eBqKSl$~^BEeg5%~MQbu@DC|`{|8P9pyEZ}T+4N*Q@1vLI4ox8AX^$}Z%=19}jzDlDA|VO!bNKo?c|knfz!~zK@5m=3S<}|x4;_vSU!jILB*Pjn=wOpqi|qwJ((60^YvuG-VxGfyYL7d7v&T`*)<9Br36y`m^{#}Y4UcC7n4@Q>y*^8%N~9IU)v7ZEC~e8k1$~3|E>j{{K~`FbMv^}NeBB)16TRpXNX0g@P~<LV{vp02&*hMik(|*jO!-4!+bMkEH)1*JqvKTP=@dB~vSA(1TvN1ivkPACWIrx59R%&G2QX8?gO}@>bG5<f0h;cw7<+`p0r7(J)}<K71xdqVyPO+efaa+)s(kfg$}UV2_kjN->yUh&&z}W^J3mLJ7zP@*1`t@@nFm`D!F+N$)-pLG_OFEQ6$I!**9tN;!#H}dKkRtS^uZk~+`iP-Iku)6fb=?$v5>&ZCN557D0G?nVrRgW?@jn{znSmt@{WE}UuzsbBk8o6H)rFb0|^h?7xJ-+JY3*y^#P+k7)*SXuM2`&!#EcUpz`q6128=1kVVz&Tt%U-Bp5jFwY4X;j)L`?oOgThSqY>5iB})oHMf|(;h-xr9aeKGj#EM@W(al;N-y_h(w&(dM^SM@k}2}S9iMRcss@*W?+ON%d%(G-@G|~el^~p2qBG547+;nku$gBxf#8`)v!+*hWf7*1juj-g@oHs<e4EOMv)ViJv4xtfmR}6=WgA?Dj52Hv?{9y1_xXP}j|n6fWr>x?y1ocitdMfk+lrN76ezKKSakEQeqOGFvA@6l@y&(CedcF0;sF&(DKbF(&zva)Iv)_=`aS$k246sXB=XydO3Cq~**c+W!Rqg&gSdP2w*%m7wKt1dCA%_~w|93RrlO$8aad2kdwqA<9rI$$-!3!3NxB($+l|mgxC7t3dkYDRcr~M1xpoORRynxB>+#~*AGTC`FwOQ~`ZSkt-s=NM0tQE8rn6g~XQyVy7?B&~ionh3yv!u`32@QcBYyd)R+J;$ChFZK*yf^ubhX^`RN9jO%okmA5j{I|b@}z`a96a)gtcMJsK1j7wpNLnm!6ZnjjgaY!=dk>J&c>>78@I;bBWkVS7}4LUDfK*?F=rD<=Y!IMtVmr*Bi|Q|K;hMsSOkaSYUkY#E?gyw%ws`{baALT?$eMHD;JVM*<wAjUJbG9F&fclow_Zj{^2V1~&fMay9z$j9KlcZ_+G9i0lfE&Put-q>$uiSBjNwaEU7{%1U2_8*r_V{#;<8Rydyn6-8Gi?m2ds$WYKp&aHYxW;K&+l)DWvGEMf**0*R9;PVm=Y0T$ac;=(}ARU71#8Sg0-SyEO+nb%$drzK5Of}30<v?0YiIX<M%&A}T<HzjA1`I1h1%)QS%Qmi60OxsH1IutJ;fFvy3H@2Rs!Bp|35BQGhT8cpBQH>S2LI01=hzwHco>7?kK!wO*K;4U0=jw8+E;y)AOLxff?!A+)V4*U?ORQR@!hrk*`Rm5LIZS1iEvp2NrjZMk~|Z8I}}|iSqT$!BH&aDa}u?`1d#(|9b$2b976?w1rP@yB$f6gKc8G`<YN)FOPwKqx!ClFcklo5B|pfcQWy!13s4V-^E?<S*0sx}u;Ynb<#Md5G+xtMz~!d`j(M}4D5<1k)3NS-d-kq3nmBs=nsz{!#jDjG!e}UF3^b%F36u*3Pn{V9fa?KO$YTHIc?)T)YY#~^Or%MG&iVq#FoH87Uum3nsxs3Rle+QE(8_U19H$saSt3}1c6S2XD=iqfNYy&Y6{VJ!VMS8s!U*_%)sUf`3}m?*aJ4hw*ATO;iB)MWR(OT*d@+LtI=V&>O$Va7!L@{a^<<*Dfg)q%l@>U$?c>{e3Zj(RIeD=5tUTm6XP_@vWUqq=ht!X-)O4SCFO9Tlk=rQw;JCJplGKAyRji@ecHsG9FT~9pMi=~T`URIga(AQVIg;Tm2wNt-8*nC<af@4M2;w-%)-uWJ*9KAHB<70xWGSNfo<?nK_C^u>6UFyRB#jn4nn~;If)!t*0)%dSMH$mvo_UT081xE+li<Wwp$#2!f1J()t{M8rS@dadF_FS;-*<u0?~1kMn7U}Av<x8{FaxrGEbi@?^SRi(%?d8a=uOgwY6QvnX%ghhBwrWpk`{kaqcT_~D_5$tcMQ3?#GV3I8}axO`>GA))>fX+GZPLLuqT*ki#9jtBqcUiYAc<7{BZZf?ZaJRi?PCl_Pv44M#~ir!y+%5ze0m0oM;>es~kd_Y)dUbwt;eI?)_xGLNpVYcm__j&)HeJ6^Fk~lVZj|Hjr_$dQB*@4hkF=HfUmF-bC70z?v}ng*&pyA#58}Kh^7&xLS1H^^%8ur*@a);|$(jVEvgjQrCmpAr%nlx|w;6HJJja0Mf+--sL8Sd}2#x=T^>-=6`3D`kAL0J_A~-APyTuPJro5R(VYc&^1jwS#ILhGNn3dfwzhdMPkw!y1e8eyae3TU^K5db77|it1QfAt6`cX-TqALap}<M!pOnn2qb>eEmQF<ZZeT1$fL%|YdWp4)mDYa2(eGea|W>mQArKC#_MxQ2m)l}BafVI(5MYh4@*}-a89>+7~6%n-7tXK*rx1p0*L~8=t#y3;|Mr(*q|ca8!xeCRW5%^m2g4Kd{kaZCy^1IfG~Uj8j&TdwpQ!B7$=vIdmZg7Q1qeW9Kc5i)OmUYCK4SQ)Wx+cyKMTT1<FYk{+yzL|B$A4gI4Vnb~0wi8iGb$gA+_Mg)t#efCC`xz20~sG8YF}y{nrL)Ls*&g&l*d2%I>av_dFyVg(Xv-R*Os{SwN!!*!W|Sn&i~^M1;=4F^9ApJoYZBx=rL!Zf`|uGt=kNyoN;V3pVv=oLwf(iX_*VzOLjQ*4S#X|$szn-biP(Q6HTW;ke~`~dbcb&n$qlsjX=9Zok(GQFTENHilnF&&KOXm@dFf#Z?Su>zSbuo(LQr`fEyX6u^2?)t1am}B+1CP)_8?YWKNx=S=MLm1eMa-Uva5HxY5iY_mUYNrpjl8d{n00u$%bQ4dtJ~Ic)d?<2couecOsU)?d%X}D@-P~l`oy(caONXHv>;yo?%)E%G{dM_zS4x|VHQ=-E!;{9n;fvj68m|Oine0up@E>=LGccH9t;p=Nm0+fBPRhk4&Y>Kt4Tzk)Aq^vS__|~VpDyh3d2J<CYdzFo7lyxS6qWxl$b-xTmAgbuOjNF3-yuH2?Tde4a51WOAF;bvo0CvCJxagAG)e#s0!Uqh+sCl54$CJC+&-d=o}`in8Z$&F6VCvSE4f;zvl?IVyC~eAjf}tRj?5Cf3<XVPf^oh_jZLCx9Dm^iUE0|=QFt>zb%MH#1YDsSCRi~eu$<DcJuU;iQD}vsjwvO`dbB{e+!;&}`6>d8iD20L+B4Y{sp`HOgN4OJD6HT8J3+02*+33Kpr7Qwt}Q+jL?uA`YTZIuM=XE;g0sZ5z_QXmfh>KFFF@6RbY~1*t9rWBR89aM9<I13_n*^XPpO2@a{A5z`an;E>5N?GK9pZ&>609(9GWpz$Zxgk6Q(e0n6}>KKCB9swJB+?PG?gJY!C?@lJG!L^>$p!RZ5e1RTmsq3KcMF-EvW*OabRfjEI4lPsWg0bJB~_?y|Gzv@ZiMqE8s2q|~mO2tJ5!Y}TCc22@q%!9KC9th!gZ&>)gDJu<gk%Yf%W68+RuW8BX$j!Y>rc5hQ)TalM;d?^eGQ-L<54mBsDa?fKj&VX2zRlLeI5>to~gwzoa)^7Q{cIP3k2>=IR_E+4d;z${=A9+pgA~ub{Rj+CSRbhgiGVTa+0eNgnBG{Gy4;7{913ZbUJO@;S>Kse*Yb_HQrI}G`jmWFV2ZHYq7fm9P3i#-ge|7PtIBV8)hJl;9ilVainzWn=FBYvcBtH!;9P?_fn54Oxb3c)F+@?5BAuwpM6ls=}B?hLqZ&%rzMBmkXnIj*1_z&WtUuC3ab;y1;<Ob-5BU(!R!|U)b_fw`a`ziRmOiYag)xfW30k^NgS`=X-Av6G6nqL)L)SzozLKQ`pP61kp0D%3OkN_)BXD@z2v?Z!&NktPx$sSreJj+jOw+!A<a*3UQJ<GCWaY5^zu<+-ViKx&bQ$hD)0L9*mmXm89c+8o!r{AfY(REvXUe1pO-{hA^#g-ifWBz6&92sWSss582>5~mmcq4s51i2$tO*P%Vp{PTmmAj)^>?fT&?oA0bS&2_djxVGc9YEgMT0&|O{5pT4(cmtoMNnZHI}9gz=Fz+}H<{0d&X^-@NKAssKXpQejBLU9^nn8-E3p$h7ACbReB<ms^=EoqCOHV=!JK3vgMKf0Kw7z(Ww+G-vAHq_LtR!MF9C%B4KYEoxW3j^@Ul1yPdLaQAZ5HJHO;|WyGPMv==y&d{PuBxLeQ&o;U7!~h_OztQf+{eeQf8!bf6!+l~L2UNr>Qbf#iL8l}7Xt;&lyvYtw3)7OB`ZLn;Qv0^vZi;>-3|G@WP(!<Oq$kay@Z-~A$|ReW_Oo(H;*;yj4Ks-P%A3ie^$wvB<ns)U&13SK4yRIc5srnt6Wy(21i%A5_L2@;hwjnd_AaXwnM7r3|{0-4+iG1{!-Kfg`0ua2vs3KwTXg>WWf=&BW;8vRw-=tcP&6xKqG09v>=2+_|-7D%*eNAlMSv6jb~7VfCklJKZX&Q)=uI6~jUJFwu6zIu$RF05xg{?aM1Da|%3?*dEI){BWLsY2jqFcfxMnMuo1bzTZMmN#A+Tg#xDw4_nl6c6>C7M23Zq<T!z(zYfhK-Y3*BLgR=fNhISCxE|c{?|k&Bila-t+%!EM-zCBj&(wxll%AbaxsaJE_0PB$8+0KyTFk}O2Tv*ui$C99#PfP)r%HA`Scf`JtHJzEF7@`LC4oWwRl2OH(ECE@hYM8&d~)>Ex^FK@D}49SNf}`<Vg$BBp@cvQ!n(asg_PKVvesfr?8Qz(z`|lAOs!mYS-~335q#&6O6)Ox=|S|p9~MgX5FN(Zl(d85YCsFGYlvBss`0d1<IJLO;}-Ui_jwz0ocY_S4DCeAik89%J<U}C{M4dx3q*w`SW~@+3cx3`qL4D$e}BUQ;}j!9#Veo(K+sr#;9UxM(ManPvA@AR^~Wd`C+I@6azE$p*Z=nkF7qgyXe8yI2&hT62*ZH*s@QD5H};T!6jBH^CnvzlRF6nl0s;uL0K=&wCk6wTahqPTvJ3>S|4LaVR%>cO#{nD%aIDzM2Mc$bX-TJOoX-VSMzD%j}ye?rdSKbs-I|%(d^(Z&=HqH<KQDVzY}VW)wJPYvge`E?9NJ~33WWLQrk11N)<6msS^|Jfso?L$mghFOce+7env9H?o~Aw+1!1lLTVjB8;GHHGHk6Eoe>JIbQl(-t6{R{k7E!`hM;bNLv!Z@0b8$y&>o=8K;(~IQOW8lwIN`lt6@9fw}Pop4JVC24@;}RYRJNuBZQ3$Y9Gq^>D~nC!av||`oVe>`V>J1)*8m^CE|+w32Y&8NCKT}UFE=%!PK3sg@^z?^#vAM*4x@-s;I9+Yn+Te!H6<w_Qo4PaWTbw+}_R6eUudnT%La}ebeLbNW6n060xGXm+l-7Pzg>2&^LF*a!5ZWx$<5oFWk3S8q+?wQjOR%hq&ysZa8DNas8dT`DBm-?em(A7<9JP0S&hqbsY^`vvy=qfA7?tBZW^lPT><Rh@<!{{UsC&kBh=Z)e}q8=eRyEQWvFlVRqJ4V}U!nB9L>_RUt+6VL&YnRf^%B{5U#`FB_x6LyPghH!{*^gg%%!jHq_<wMi?S4!^sT)IUTQvBMpAxG4ekabUwIrlUmeW-G$f{DA90hyyF8K>k@m4#g(%<aT+!cakCaLxW05gCSHRR=3A0s=<5V8ZsVs$@a7FXi;^dWI13Z3r%6NsZx*P=vEg?<RDu#5HKc|QQ-KMHegSIkSAXu!g|dzDv;itOf6@Ph>%y83MO>sq{-MFYYc=w(K{&<dw857js!)KW4a<DS)K^_8Ya5nX{(xe@!9bm-tu|MiS2L+7(wkRY5(wcISCxTo6Tc0IPj4W=OE%K<_-`l(L%9+oXDU@LddknW{2p8Q$bDfq#OvdEsD=@5L?qCZDr<@2@J(zUcAm|pX#g>w+9lwzHhqMU9gLa#yn09_$xgp0~aZj6YU<$9Y7k24GcGn1RGMOkvlfKDK-XKB4$NNhK)_>V4NCJwL-mJlSGqLfG8G~#kZ*0AS4e^u$vZ=9Z<ditm~V1Z#9!HH?G`Tx`h?UgNM#<cP|OXAHY6>DX*91#&lFnkSN}f7<D9=`VANb=n2sgKOYGn6dx$EG^#JD&4@ExIB;)P@9UzRU@D&%<^Jx$%O%H1K?Bt}%8WwOn7B&CuFA5ZI$7)m@!)WNf<U_)Yivn%GtB{?LsVy0aN(<PMWtylvIqQcyhbLJ20@*zsLsfO8lK<%agaw2Q-b%vjajyR-K#^}aAM|hQ@dFoTpqczrg4IdB|6kwd03qMR$D(!Te;Fo%eLgW->FbTz(s6{nLqXpL`M-1Q$m#^jyD7tmJYntdc0(7hux##1fD&CSB`4T<u0AU$w=JHHD90!MphEX>$X&2+YEtn4rk0y_jhkTzJ6c}d{)8@DKT0?SUXRc_=RXUyHp3^Ao`ikCn<Bfa#f*RvqVR5>v%fA2sK^Eijs3`>NlC@&IK^2K-Nj7?<t}Dl<`miiE1P&L}bVrQVDh}a+UK&MT>HaJ%@srIN;C_2A$Ip1(-+)5lRR<2hDuEMkpO}E=k;|4K4kg@jj-AGrTs}e98^WK=whk?=Hfcv_TqGzxI86;$)U_R~%vor9KX2EKA>rnxnPPV!MQ003r^Op=+lMCwCDj68s!z#I;Cuf&k|~aaj<>k!g?N5q!1aaE}>x`o#-KSjD0JsF<6ju@W(0XO>Y$w_BJp1+Vqd2=jp8xLqLLK(>RKIZUgjg%enFu;WTopfp2#VI8vJuA@Mp<9iuZp%g<o>BkgzXxar#k;`feYlcBLr?u5OD~42VUZ#NQB|BSxW!lWmH%FV<o{cuM9m321f7%R9q;WB{^RZ?M-4;g)(HI;Wza0%{`s5m)CczMROWWoy6$nY~m1*8pbr-M?GWec$pCh%2$nBFGfjdk<wuK26P=@i|uRnpNFY~d_Z~H)%@S2?!yS&>Cf!7g|QkAXM_$fgFkIpjt!e+$Yc`um6l;*YO4&|OAo5TrDJytpyS7@r)4gC?Y3otn?Pz97z;}x{7nBdtUM?vzhl3YGra5WFR*-@wewxy{IR21<m!BBL$FwnL9kK`^Y6%NI-8B(GZ*Obwwi6#n{CfwB3gv@HJ6voW!e$)nWeFor|i%K331S3Ox+EMbbqpwtyZ+Vsd1&3yvacDT^A6!Tb?26B^0btNo(qW+jU}$IZJ?a#QK2K=7p3l|z`l)Y|T+>4mxe7$Jdx$pMF|-<@tnf{eX>K07b#54aM&1*9#t}3$iq9Z>ljnnXGiip%-lWhVE^t$oD$WC4ZYNz<?h%nAM+)i2vZq0hpbSTovIZ>q;=Jk(>)vb<eyW|YGJqW8R;k1&n|0N~5#OSXWi1#^iUbL$bU&rLP^E-jwXo<uHAlD)Qd&%5A9-I~fJ#3)TP<U};ISE{X)mXJE>Wg7AH9guSv9fGcq1Nv1%G1EY!+0Jvd}TgnVwIk+Kw7GZx%=iNZsAA3^ItO2si<v>CFex?XwxGo-^$6PH!wUlP74)4{-Zod5AKYJf9^3?)~ySWUw}4z>btW2am&{b#XF$48n!ui1Oa+fSyt5+Y~g4t^Vs7&K=9;CCjQD5J**Fo83gr_af92lAzC4fj;p3_)3a78TnP~L#a4(Zghw05oa1@b+db_a;1pZ;36N~ym{Q#5wj*JJ;=FMxjCkGKeTwuhtF{QXzOoU1fPJ-K!k}w3vDhpnWkf$QKlE59NA93v5(hp<MnpqdtbVR<<1NC&geSGs}dvx&VskuI}4Jhvh=hV3+aFxt*FRfSE{0tg_0D*gH#N95T#6{Wg2La+Qi*Ly!hOb+SM(<=54*m)nZWVO{t}tO;?1Vj$h+ZR3%gOI5XjcNa(1qsqZA4!V|Dn(3s5@grhs)(0kXTp*ZxFwwT3b5p9gqdUIZRDoSdxyG)q~=V)Q2L~bCMwb|E<Y$wJN@hnPh>7XntQv-5R6x2^>^}3I9pPdz;Q6=#&JH_b<+Y}{%VXqN1h(<xvip~LwMqF8?TgKdG5gQ|;qzFBr3A(IgUYBd>NpvDOU$M<p4}7ze&eG6^;SLYSFHspo#MvfFv<4G#i28_4YWdC3aCFM`n<M2!$5qhl{aYa8B!&9j!i5n{Ggv2L+Fv`j{b4Hy*Mw|dP9S%~^i3R{USdN=bM2NY!B7t5!L|GwvG%FlRS-2tIwKj%I)s!(EZ9reF=ZO!qJza)sDmf8iO`hNp$xDmK~(hQjT3F)zL?=K<>Q=HQOXRj*$d(xCKU1fl+x}ghe(u4#pO<Tw%Cb_h7z1O1}(#GCpOZ{2~>oePc)~1oC$>AIR>d<x+Uy)X5XiD7cRr{$D&U*{|um?j&tZ~-d8#t(tZU}QpZfGmFbmE0tTpUr1Cc5B)Y*cuL?JjVC~dH$@VFXOqW2zW*#tbf9;l8h!FI=JOAWhPdmeH;XE?`R-@OYlnA=|O#)2aR3MSj?kV`%bpcI`M+1%`m4O?q{X-S7n2bvs_-8Oeaa_FsX(&gcplmJ)nPp0>3Sbkj(6aS*GWA~;gD8x;6AU646hs~nyf|Q*-e-#>o0>a21{jmu(6pF~Q=36rXzpW|SO7q)qK0YQlDQ;L9GBS*3Lg^jKonF;#(wP7!mlaxl5Znm&{(AkIoTwm#-TfrcuZo&RImgL+?UQO^)BNg6J0SVaA0X{C-*uuNL$TiKMd6+8Sgzwo&+~Vt4*=D$VG)wk}$~$P?rrmSQr`cTnb2(TTLSbop`~BM=WFJjF3E!G!hPpm0S<J7xGL*um4ZLSVb>l{k}%Xiwjh@6?Sr|O$G!5>iPulRaV+^<ZZDHEqSKHL7u0qDY6-Z0_Qc?edvR;h?0^v<(hf7a16XddeG5g#g3w~=lgbRP=Bm?K!Ey%IuYC;N#R8dC%qa<VftOLmG&Ve_?u)a6;PxFLY0S+wqKW@^pcflk}2TRm6E&@`QmEYDy*k0&dQsV2a^z$@t~0&Cd?8rJs9r6j_$Svh*qsPEZ7gWEAL&^NsIStx@?BC*%RVC!c0sNrU|ALEggIr+l(%`qMT5!pCP~`6Am(>m36dw60t0T<4FU0w*U9ai|ru5P<EErd&chs=EckT^5jH$iA`!s>(#n1A+ReYs$`Wt_;o;&salk=AZ-4oY6$5sl&e>!>2DFUIdz4>eh<k(XHu)Dh$zb&fPd)NRH@7LrpmMQ$q6u*LQgO*@slg70xK8jM_d0QukB-KFLlX-TRxIUsotw3X&+h1?0W@Th`T9HMNqoVY+J5w#?L9R(Y=7bn{0Hco3VK+b#nz9C~AuwCea%ArH~?2p!xM1l4bcvj^gy*f=|oP(J9C1s>Vb@+xU!3BnLur<%=?4V4?W!8&EY;4L}pf#t^xeJ#9H;U}jn>aTthXm%g<cQaqZ>*S?j>NmnDuNh|>>!W|#u{F=NywKD<-D#1_!o;Jf(U9ik25F2ol7cTqf1&=3rU!H6evQwVVSP>8^+DKsy8s0_DR*ndh!=Y%vmnR&i{y`q`Gc>eB%%}0Gip<WXCLDRV0b%!K8fH@)<i>SI`E1>}fX7-U-X`#pv1~Zq!6@5*j@2l1S7EJc&5hEqHmU3-UIHcHWI<NzN4fHI;83cm&vE;kVo5h2o)1)uxI3rcKXqJ=mojQfsOr(_1&)rA90?3z(Jl9gdYAiLhl94RjfR?{S1zDT&5#OJ6LLEVaO834;715}x=vXYARW!K^fG@gGmB35dOh1$mC8KBi983ggf{|hbuXbODj^*}OmzBxOiW1ZjAhDvjW{LBrf@ZrM?ROpQe!NKO^n`<Pf|)W;dN)0l(S70eOfGl3Wq77!ZF2y>{W!u*Id$(f|j9D4Z1U$+O%g_<IM4fpv;qr^K?aGz1kwe?~rCBauGen0rTw*o3+r!_pTne6AQ0xyCg`Z0ANq+gC%%c9=C1Eq$zq(d*il&HF`Vi5J2=E67L#%*exa`1YesRp%I+2J*`f!6cphd8bkXNi4X!^tRW>yE{f_{w_1@BVB}4^X%g*t*OZ|G0g9xk1Z66bq8g=v!Hb_s;;}u7t5RvCWwttR(0ZOr?3n|(i5jU4&S;mKBbrhPL*%gyQ-z}CKvcs$T}Qmjly0*Q=S<8eD$3*6|ClBbtTj=lKP|AO5k>ust73LM<f$jhJlZI=?Y(tvi38edB_?~MHaGH(M?Knj+A#2qseTEvF`}$8^s58#3j)KYyrT#<JR54%5OK=6?@YU{(Bw=)>Zz#|NLN-zG`MryKTC-Shkfwc&}Jwz!B$unk*CcXsl0-E*C_)KfD<#i^CTrZx%HH>q)y1kD*cu1dbsMZ+hQ`K^B|jELAy;fwCkkTxRhR{sV=G^06#S?=#B3^9mpE%t!jbtN)(BPGos^(oJfXD!jKWhWMjXJQ;xZT7=@a4z$KPAxtncpM0dIpXRm>FT{=xtp!o@GfOk!fVi}hsw7|I%Ho50qCK?XJIsZJ{iigbnI89cncQ;;xc&o9YI8Uc8C6+Z#0m8+{)jV0NI0;plh@h^Cjt*lGL=&5bw>LCM?2t7Zpt8AW@g4~5m*;aNVQ6b=P+(MMN27#AIqR&XR02HE^6%XBXPq9o{sQ0wA+UHddU`+M95=2$k2y7@$=~i(T64t@+tqvXkEnwJbfI;cuD&uu{UIm_YBG}wG|~D}b7D?DbX69e0Mc`L26>vb41cjFMYm3&Vh7~yZwn97x6_n#Ui&x&)IVCot>LNZ+<>dn3;<4*s<4RBKV=J#GC^X3HN>F2Qf{hR0<U^{3Rei&NjCSPL{2i}9vn3aXbsq+AW_H-VRpB+1t?TLT1PDOeU-H%RbX9iiy|}tJ*mKwS~pd6WI0fFws|9=_4tWy*>t=N#1=y~e7ir^ModCU7F@QJxXf6sP`M4tj!oTLub&kLfWLCQ=5!d-j+i@?=qDP`tpCg&_On@U!xZJPsnC=(`RQD*0BE^R>bCPf>fVloP(JpD{>^9smHWxc!q$d60_Q2tf^qUwbNCW+Zv)eK{6E+^6M6')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
