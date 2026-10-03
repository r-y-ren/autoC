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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-q}vO>bOBlKd|`_d)C?C3$bO)ME)Fn+8P<F>4Tpft|$yi`j#BZ;So!D~tW{`ekH9WY%lS_DKzj>{qWUt12@xGV-VYz4-TEe*Nb^e!cjYpDup9`S|hTadq(@zx>y~{rBe|eE#^)Uw-}1fBetq&p%y!`|0mL|9E%%_S2jDi`B)$yY0>Af3F``PyciC!~5@VK79U<H@6QLtINm7|684W_4_w}{q*DUzq5yY+<y3Q{PxT2+vh+2_-?!X{Oz0H{^Q;IyX^)0FdN#ppWc6X`}5~_zyI{**A63_jC%L|UmnbVcpPB-J^rfm8T)YaX1n{slR^D(dw2it%j=*|58IFT7mwDYhQ-WRZTAbClYu-vYBl+A9L8)?4ND3S|I2p!_Vmr?D+QmtpSP!3Uuq_H51QJ>>2p?Sc)Jbt)5V(`dlq&>`uN-1uP(mdez^VNVzt(j^Yn-n8rW>1ro)i0`SJGCiDj+wWr(j=eu=rkUE;NU+7pNWAuqI>m1LfNxIc_;_Mk5dSDL8F7QDIN-tkA2r)vI9lLzl+5syGUZ#U23dHZjGFBo6zU>p1Ydiq{(_ni*qI=uSqR+`!~nd#mCsW-pWk7I^Xo@wKG$M1|MES=xp(~_@-KLL|!Pha?!ReaUbjywMG@sNr}3T7(VTl)c?Z*st{nw+m-R^&Of|8q3v<5!1IwQnR}WPRnE+YcYMZ|;Bo%l7X6{fGDedO8QEHeB`I-rn8*Sn-cKSH{r__V@YWC+K3|9dnbnC7#Cmv2wG-^FSF0y8z?cfQ2e;Nx0Hsx)v~+sR3?pcHe&Zu=f*Am!RW>?!FQ}SH0}qnOPU?<kTH7hJ|1GWK#Cao!(SNK!Be@Jh*kf9@8;BIWddPPrQW=Uee)_d_KU#*JKlWUOSi^dd!gNkz29$!i7Vq^L@b64^CA)j%L48@;b<5jyN%3xU+HBzBYWx@x#E&ldtW({M;Woxlr{<9=|Z2N&baq4G*|$_3u5N^z+&KBREnZ*pj~0Lf#fYWf(v;?tdu{FS$#k1u)Mm{lAip9mWq{1Z=hpXwhyZzj|!H4Mo02+_NovQHLWUH>PDkMfLn_YCw=aG!M~>O>M4v(FWg3IAz&?z_`8f(h%i~dpr9eclOoH9s78Hck}S=_U`WQ7P1R=AV8exRZw_*gai(r8$Czg-Q4|+*o8lW;}`Lh&zP3p0QQ&l<d@X(A8&jL#OXN)-#DFM_`{YfmAj?Ec{!Pn{kc$j8gtsg%pG2C`G-t=De!iS`ONzd$1}9!>l+Ukx$~XxkH$CZx-MsDUB|ZQKeOcHGq}0{Zzisva-f(~nz?Kx=q|mqE2-i2QWqz4m#qO&N1aSevJOS3S~^w7KURKX4}*^QUP$j6KwlxdV*ADOU3n#3R_GZR$R0I4hRPmsuhfl=&YW}e?blDw5p|vdx|Lmo<I@xu6(!23Z#(4J<)n!aj6}3@dIJhycaa-6xeZ<WEghX?gc`TZ%=PS#cMbQMmtz@!uHu-qo>0O0K!8&6dK>hW6xAn>9DM_V>n-vIJm@IB5Ab=Vse*IWem&}A6A)q*egA@sebrCP`))Mw>nkpG{PPl)e0&f>T!j-|qo<I&|FBcrU^Vf9nHxUj>mny6XE+w~`5I>hX&z<Z%u!^(mOi3whnc>B!A7xZ5bS*#6P3DZh<)eJTk^Hg7XgP`BWbS@@^Jg0%%2ylhR1=Z0p(EgTw@LFPxG_UPw06#bjXsXK)yJ?z<LlE@&f99%%A9c<%i$r*LJLddQaL%Uj&rQi9+YVCT*wcCaIk0I#G%P*MQrIE2S}=&I28wwValBoH)<fN*R3CyD7ITylLil15{DoPyolo->$Oo@s94~!r>hwxrt*hTzQi9mL{1+Gd2C;cvI1}`5Jl>ofpp$8_te4ye7iIv~uXnyuuh)&w2;HU||$II~M@R4D1j03g^PeD;VaV^BpQ~r1gjpA3ChIP1B8(jwR#*r3DR_=?`nHP?nP3JQgaR%*U39W!X3)6&7TvR=7M9<+ZG_+}?iv=cVFyUcSI=>lg({%nJPNXpPX}D-Sc1i~=PqceBp#<uG5n)ZB-gAKqSQf8_8CopU#+lE@~V`Xu}cZ2^WD;{eG5<@(1=6Rdg;J^=L4HjlokOpaaq3=&Ha{zTVE&u99(+uM)Zrg8yzqr=w?&9qSj3~XUmSg%PYX`yZMOXf)3DOO>vIjKjgEjaP222Doq?NNXg9|PdHTc3>T&F%cOB24n7mx0OzgmTQMZ^4;aqp%w875iOwKfb^H{^tJHUy~Tn&!!zE#gOr#JkWfu)XQwlL8I(@SOXwe5^XHn64)Q!;Ek!xl|EpNZ(=yRB?f=Cz!1Te1T3CVsb(A3Uh>_KKkxFp+k4;y!VKP*`PltQvchrBk0wG^Uk3W|5=3?%jW8_mbok_GkYRhg_3&ke?T&LUDl2-~TDdq;Am0y+^F$(Ly1aGikoll+`NV7j<4I4~6Ct#^_?gLSa2h&V%;V1_sewjbp2KjCFdhgqq;-<3Dkg6-nv<cilt=Vn8i5zX0$O@esx;D{B?d*b`3#NPN`LH;ur$OeH@NHBZ|Ijg?ppa)5`bkX&qZDWnSz68czP69)o>|>8IazOSS38nZkx58IaDZ;&+fzACWUt;OR%ZbEU*m+Gy8y2I=}nRkuoGSg6JXUmd$Er!9->OoQ|H271z5NU<4=&;6r+>o+Eubt(CaJbrgjNu7cgI)N)DeAa01`R=$}>q|->+LT`|_Sr1uQ02F-Jxwuv4hf@M`6Tmw>`!FYLm7&+WO+#frD2^T+D9l2r?ue8SJ9>b=LX1^%281EWVl2fBF^ZN00qTmDjdiy8@n;qg%<~~fqyTvVv`W9hNCt7PrS;b<ks&-4cyW6Z;6I<appFDIB*poUH;cUKoyd~qdS`)L^w*21_ZI*C`wxHpl8)oCHB`Zq0e97bJ`Bd-2^1=S*o$1%Qkso`e4co}dTiI>M(6ZIRslNJ3xw!~?-pH{!v}O@jYQ!#q7kL2=;gUYl<h{P3a~h2>;c)rnlrSe>SlO+LX_}Plg`saom!CSl-1F+3b<7e;PGwJ6$hg@JyV16&<JIzz}%ED1TfX!WFkUTe08K)!EBEb@m$OU4DI9u)@=TwVPa-gfxm5(rv-OBp5ch7AEfF5U!q%N1|$=s>lvB;6soCHy?c~vBrC@DFoTdfQlSr2<BMK_oe@A)G0D3kc`~31p*wP<S>#;#c9K=k!ii+*W?Oy^%P9FgN#y9PIw>q++?3K$V#wY?YXGjGhoFuq<p!KAxggL1yR^10tqF|>>BKV6pvp@J(^EDRoNsWnz9NmVz9J7CG`pGxQ*KdW9&T<PsSHKW-9X$I4@Y4G^-30YLwI8KUfEPX;OFKlsnNlsVfKC~gd@$xgAdUcz<L2h4@vI;(^oY3C4d1YzYH#Xm1}I3>}#2_tt&-LnEv81rC<%xts_B+MmT`T-$4{IGd6hgU21U<nA=mGBJdCHP2f<@lBs^)e?guxz<d;9p#oeIDEZsRN??%O=;Ve<J<r<CnvuhRoi9g8PE9myNyu&6l5|*~Xe0Kce&17Vy5YGH+m)7H<R;2E=Yng@?V*yWD@Y0=fwEZCG2a2enkk1A{C?92((nzv2<OumwlVVDr~U}V8#|0y0Va{46Is@Ds7X?J8m4R1p#Dm6DOkHatlntQg46V}jZhjIokQo7Hrv?>ajG%5QJ!a8Ki57q>UbvhhwEYKpA4u(uT8cC*9KB{ON*1#AG;X|<1J2Xi&qYCyQ7>S6bx;Lj>5g^@OGyRA}2@4#E`tHuE11e;URB5{cTAD7zDBSN#a;zQLUmw)OeK!YOkM%!m-g@O8<uslv7YFn9wgmyRt{<rBr~hYBW%Fdr+~sGwz|o$XGud@FQ|mbu~Oy3KzM>nG!zBS~uxn69+iLSjpJ&<qWYo9tSSL?>I~(PTNvUPG!RMFo9V{CbBV&k>H9miFxfu%~r+GKp@A0Jj$tb`Xkt+4n_%91fS#I0sv98<l0kwc0FU)R?-75aGXa${mb<$Hquje1c8=AH(50v;tTADeOL|{tebhV`5L`k02raWTb%2_#*XMObp+DBej~4ob2EAO`nZCU|9Aq1<aZf3ho9z(zn-q!wXx)gz9!*U;}D{!Q8mEcQ!TFDz?=3}QppmKvIkOBz}d398J6i7R@pd>Il;N3F2BRhof`D`4s3RG3~?cBxt12G%p>}0<N1vxv~nI8zaVi#L(_!N$Hd+2CPs}HJQAqfUCoqosP(J%B3YTygXK}ks+$77#c71BdT1-nzSz!_wD`hBa&9BPxQ%KpLF4Iucv5oLG8Pucbut)@m0P^3=nKGQR`)H(r>dUfej|SKINCn)BqMiqE))t?DUX3qf|OM2ITPz2U}NQ?B&m!Pqi5oQR!01FRb!a#-g^7pcfUcA%LU;+iHMbl#?!&5P;EBe*)nhj#0JdaoPAjhjL||hHhJartYxH*f(Q^Pz46=JdzAu4u3G&{3BeKcy;yez%mDyjR3I7p<foU^>&I@F0}z)(zy{cXRni{qdzg<_pfwVdVv5GdE1EF}0RKyE5W1%+c+EXZxx0=^zA}(kP{lSCtB|e_-4lorDRy`RII9M%MBjxbHi*cD-yPUUCqt-K+^4g!B@3H)R5r=3L9g9LPkNwF9zq$lD)?BNo@R$v8Vi+;_$-Dpoy`-$9WGK;ipx#|#_4LqP?E&3R2i9<B|D}A#a<oy!Ni&<D#g#Ohmqj7K#P!<9-@KdVf$<YkFLV>>o~Z@OHFW@1VhG>ZQD|6KAjZvC<H!L4HKai%#_iTEg~^;$o~fa*($siC?&1SHb5{{89w)uos5g3#B$)q{n=7QaUdo*!EK(mB2K2$gm~Yv3e!Mt*h0S+z|1MCK`8g;Yyi`bT{A$?MbADSk<G(MVoI?!3)jl?U3p(@5^XCx3P}pwIPt4{fwJtH^3Kvqr)Gy~BJ9!i3Lt9buZa(l02v5yd~?o~Zmd}l{&6vp_yPGF;jNH!iRHVKuwvd|Y1NFB3{XrbB}ldf;h6;;0MgcmvEnC2bL!>PGgRs?TCNUL;k3kzB<@<<nekXrhczTSqG7@?lQi*Kj5|TZC55Plig(bTbLfEECEM9<Wrh!Q(u2w?)|gI!Ef)0btN})sh?WSBGqnFmsTjGb7O2V<JYz5jgQZL@paf}EM3t;9!#`<6wLWB9P!HVLMC+I}`^rs?B$x+|1m3ADnov~-86FJfm7pmPh8Z%&E0!a~q?{$jZKB8MMnN^K3gL1TpgGiLr?>d<SRS51jfv5m*uMkfo?h6TbVF_1`ou2q%L#<Azrrrpb6nwSfzBidDc~$2$Q&|&lP^QQtjOZRubJNVDJXR|GEtmi$bL~M6z%zu>d_MOu8@I<-wqIF<<pyCGhyF&FkVj)K4q5>hg2PF2vR#6DX3IT1{@rW$_Q*p_y5WxZ01}_Ihs7?LqzmCO^5=JgrZ-dUA9Y%9V<r2p*q)LiU`?ohbgA^3P7_|ETIBvYD7FYvucJ>(S3v%C(qtd5Qe)jG}-U;!(h>-KEN6IpW+3nGo0fuZah^OH4J^R6((%Or7Ls@w~1Gf6`f`zkG`1V7raMVH=vAm&lienwY5M6)IXT%Sv0WKW!2XF3Q~$fL7GmXz<)9GH`$3q+k={T=GURky#)8iBNEF)#)McI)WeX_1s2JOk10s#loc4+9ZGI<@g?CcXEYb5ET5%rEWH|TJW*qWAkKEBp(RI54U=je0plKM7?71;V-J_)jcRpNIj^4AcdbN`3*`v8B4$DYgZweA^0Gu5euqE}(;m`2iOk!xP~cSoXgKR6G{#D<KAgQ#dN1XIH(J!zYpEF+gt#0>Vw>VP5V{|9%d&zxUlJ26<%5$WhU<+AVfb>`e3i82ZAKkaVHlzXfrt^DB<p?-JJt?`L!#`6x_8E4AE_KVUMFZ)PIr%0WF?y^8@|PM18xoYkwpArV9m-VyNEUel{qp}&#`rSSwUBzS-fccWzAPNDn=!}58nqQQ(g~cE19*N)+bGgZc`X<b=7c;%NUXKN+tnzK?3?<H)K4EGKY$BafQ-2QA<&3xkyMY;6?`<J8@%pj#=$YDhrc0>kt)xuxx@VMm8Za3IbT{O<@CeF_4ekPxJQ)DFLhs4XcaZO7!DWymr|YarL(aXT@U!dubC-WhD)r@|i4!C32q%ASMwkpRN1B-xKr8QVo<_=J_%hwZ%Z2*J7STil&J9CTblZ^36AM5a;s6V?h*&ZepKY*#>bWb7)Ar=bPW9bWd8`v@!KqNudy!(1I9`+wLe6yI75P@0Ev?*B7oMH%)^kk?b^*31?KFu4pxj^rjyL#el!$Z05Wi<`(c)qL71~K|7vX<SHA~_l}#DExfBACpCyvtU(^$C!X`2UAYx>h2=hFz2dgisX-hBbE0BXY&=>mup8E7@$LKX=oi)T%nSz#1N38Xfx$|Z$-*g_h7DD{5(Aei^i6~BT>$FYCiyDLt@tj<V3(RuGZp_Asqk*7$RO`jH$)s8I>w>8P8k1on6E0whN%hsaE~IwPW?%uSx^Q$9kxPL@=$fn{v}q{ifI$^%IS8h8cQLLMP+YzrzsX*`e~b-2~l?P$_v%0*2xQS4M-AS{B5|2$vkuZ6g%eeNdh7)?IuB>32F-11+du)`7HM31iE<21<#&Wyy^Cs>sd)oV5GbxFeuPkBl8!`GV?0{l)aw(Y`>e=8axx$r=VG0qPo}o;iM{;Sb3FknIe*Sbx!WoH-A9tR94{g6^K)tq~1-G%%k3kMfA~o*+J@56L!*_eeIwuX4;3TBt}pO7FkHd5i*tNV6uC}Fsq7H=U{pjk2GXlH^&I-7gd9G<(5&1zP4Rz!l<@Qj8L)jCF<Nr19U;yWH<4(8QIzJsV)5p`a>CAusaou=MuaL+YybnP;LeoY`CSJTfS&jb@=v6?>rS+_;P%9WA{d@3W_S&CrR#F&mXjes0TPUcr__BLy}EfMn=V~Z=#bdH;Z3kFVj~R6f{qVZ%P$uOn;rqDj}^BE`oe6MwHbOHyfI)g-YOoGop0KnAML3xF_>XO`&Z&W<>$7-H;*Y&nILvrRu}my_1pv2Z6Jth|WVklbp)jbDK;8I3u!lBtsgTvT{1Hch3{c_P3kr^32L24?L84P-Hh1U4Cjq2MkG>kV@8z47cU&ufd(Rws5!W3JbD+20{PeFmqe4^XYWJ>tUW6Z?E?HYcto9Ad%`rl|Zx!Uu|i68mM0LWur>S#o3gjn4c~*(SckLB?|Xcqio7rstaD9)v}tguNy`9X;4lCPN~H6U?|tEFC2wTsM|pK`(qVroCwgtMPRjxqGn`dGjI>qi{of(loH)f)M43VGnl8&;R`$jf)Qd=rb;@y43#JYWwnYwKvA2?$P*`Y0q$8ESSqd^+mtx1Vs;<uP%TxNK&X<0Vn)J}YDy<0FwePjJyCGGUY{Q3jCodorkV0Ty~c*M&I=exkC^WBrYYlSptD_BvK?{<h_{^Q!3wHI9O3Hon7H9fyp&L$MrbPXx?u1Z40JQUfby^N#i<gTOjR^b9n>wG8->~dEKZ;vqpr1=BB0IVDhE2nWsjc@9Q%49qG%Y$TrRk%2M(1Yk%2qdkczr|AxaPT=gP}~?9>|1WoHiBU;_H8Dx3?-)CSDJ)%<N=4Z}iTm0)Gx)kPWcjev>Fy2iGQ_(<lPt3S(ouT~}3l;S3hEuq`jA`LLn*+L8Bg7OF~D#<?Af<Orf+4vS<XV~_X*H9ouQPO378N`V7@iJ>~3dEFZ7Q{W9qC;e_2XeH`@|-Fz<ZC(6`Az_@45;a5nRxESOQv$TrNcQgbW3>p(rt{A?^A<Z61z9#+qYN`1tSPSE>bmKX7vYy9<8xIInT7E7Q~5YJr-^{8RgoRmB9|<b^C0Mv_z~{v!hsf)#Wg#uF%fe(5#YGi?oPtG&>;N<tub4E{I0?Spp$4if)dsELRMiX>v)FSBi?U5pbw&@Cng{-p$BRLRmgj328IlJ${`4;W+X@mFD`FmuMdpnO|IS5nd8A*v4ujKEJFIxX^0`$;-WTn;BjMR|H6jYPt6|@NA)?gav+SUe|Xx=QlkCEI-@oWPEH4IF5fl{BQnj7!o86$$CBB5TVF0nxUDS^RtdNOi+7c@{er1$s!!BN0qXKqIMPat9P+;$~0`8palgEHx*2EpayHcT<A|_*Fg?4T4dcxftS5s)J4%J?g})8f*a*PtYFK}+<OhQ8s$vzGF`OE6Mzjx(IM{@11KRz^3rHw2FQ{)Isw>0+<Nn0TEZ(ERRr`8Brq4G{;V?y?*6=Z^p)q#uJ%m)PiZshp3@?2pB%6zxkc(^TJf-oUTEnv_J@I)6f{_zM%b0e1aLrk9Ru&5sB~>cn^uANBXtiPC_P57TxH2**bHd)1GiBD?faJio(u2komg9`(yz(cLc=MyXv_e;ymuhoHLFp$-L3-Up$R_tXx777kYFB^ONTYGpuOzv&k*A}x3*x6jrM~Rz;f73WQl6vt~OWMNLBN^fFL|v6sg7I5~xLm232w9NDn;)tl~K&T6My^$~jgqN*pU_;*?;OA*M{!k2Ojh(R4>TUQg5XJZKgJt{gxFz@?UG;q18o@$UBRr#JUaPz#7Qod8tVLgihUkQtpC7!{%+wqQC}luC*4?zaNhC|RKU+Cv#GQFXsA6IZPnk)ZN>a}y3!r(t19h^d-MEEB2xQb?*rCo)=DyJl*8OVCaLd6||j(AK~$7Fh)l0;5$H77?RDt7cG9;O`f=?90~*_xc62*m|WcgbCH7j&oh0U%-2ivDQ`pU=6n^L5ZsOWK@Z*FRrmf^pcTh%y#jV-6YC%7f>-N95$4P;I!{;^#xmNkl3s*<EJk60TNzma^=W_Ek_{d-#_nvfnYDMf>$=FEWnL6S=ZLP(I@LxVjC^tK@-qJkR`Z=Y(X{Yv@s1G-UHCwJZ;}brml(t-LePiXoX%JPmEe*|3F=d)s$|hBp|j?!uB^y_c}SlO0^&dhVYa#W!;g+o!%W`U=X|?7iJV#N?O)l-lKX}3q+(a^;#=Tfjg<D3FoKG9Dy*qPhv_Od##9L>t%4Z2K@BZg{mkQ3DKg?$_uNcesMBoK^j<q*hU#)E)}T+yPsQ%iV7ZiT&_WRDZhE2)$FI0a$in{yVu;>gYKHTX%wiYd99pDz#-p7dR`IugAuOStDy_Jpd}^9e2p+c=&+Yt7uu|MlvVCBt!&w@vo;9u0yhBHRFk)@M)Mt=Ca)_4?(!CI*`9W+DTyLgWF*4U>rxvvMMpw^mqAU{#q5G3<@YQrrq$}hsGDo_c&RzGCSpaz2ej9yTd~W9+|5!}JiA;L{W;@cs{OpR6~#3Nf?Pm8nbfLxD;6ddJGT^SS7i=U84TXV4R({Ah$OX$^x~-$>7f(6*EbMmlL-h|l}IXrFemJ#FA&A`<Jplne89L=<XoYA7+m=pWF-?2nEr5z0gV>owb@9qN-8U*ds&j+C<qpsu*r0~t^r>8qTPiJB)3ddt0mRgVI<W8nU>^MQSNC@IvEh#0?vVrY#GWisH)3GJ*-y7se|wAH-5dSgSpj&t7dv(n=n*_P5NM>^?Csur%?YW)AcZ_oXt&-c1Xo_80mx^X^Trht^36{WpYZRU04Ufv|XAN=NC~%NJ~PV_JjijKz4wFZCfu_(vxZRS}yki;kSS-?b0!3kT>9sldzRkE@EGE%0rG-4Co(}87WQ6<2fQoENEx#+H{{Kw`tLW{JjLLlpX45y`IuZ@=?9Md{gXI&*!ufaT*mc^<81h)4+os>}5mPoQpaX#J>Q*n5WCYFRSu0P_0n1ovh=1!nFn??C>Y8)K(=kE7j|awtP{!oRd{VD;%kuJ!xy|^niQO1f0tdo<gH7-GZ`gQw|XQ{`<Ubl7q&PVVWG?&p@roajahBx3efOb+IGHZt&$jls6^4t+SGJ7$b2pefDLTJGS(Sl1rtehqL#Gqr4c^qZYfiZH$rfcM>lj$plpt*7JyU3Hc<-98j}s1p^gml}vqfn`z6Ngg3%%$O2H80Db%}aStV>BfB@12^kC&1ImW&hUf3et=2FhCOg9?YOZCME1=HH(7Tl|b4PWpV@b*xa9oQ<6OJA!Xn+Eg*q+lrohcFubJMrB1JZaV$!TLDXCAc>Xara~W)*KR<C2wm)&)g!URp@y7>f-v=_Rx1oj}`z+4aL&KL_qL<(<S|H>rkM6`5HbwUkXba%&aP4N{uHm-PxcJ;Ic&R6hY!_Wjp}5&)x2Ah6J!5(L~imdLYew?rQ`*h=owVh<U&bLNctDBVHy2(*`zmIzn%3bd&~c-SbxXt7GHvxp&yb`(89?~_)93uzy{OqGs&5$}gOkYr0Dok9Kx9BoRw3a)F5_95iG;kmMT99ByL<O#!jZ?JcWde)$H5|uF?ksMH2Zdd4d{alp@l(v*PBjAoqHBFW&&B;A#i^b%kK{oBx5qYUgv~zD&M?0=s67c6mm4>mwp)X2<MQJ4qH*Aru1+fNd%85haV@<H9g}xMQ57|9yj~JsIUEhN)9_NT+Mwo*nLg|SfXBpXIyiSmBT+=3+Vc-%w0|uymU6iaek?xHG@w)^OuUJTE4^8$tk=}Ouhr_^`>ZE%-jmss<jubn?s)H`b_bXOb<@A7-=gC1cf1cH~HRvcF50Q?8iuh%D7J8o4OV-u##H5`<D?e}69Y?IoGvsQ{S{Be1A3az3G*d-#%F`3xlQbb>`OcQ*GG3ymusC}UC{&e4HVv28E-CBPASvrGS{+h>9R*Ghb_nN~`m13q?R1vDVzC}X*aEl7<!goPyu6|}gJ|0_?em_8yR~j|w=N5dd<MRj(kE=S(Q8UvKXhbr3L>|5SG`7`z|nH7LZb|`<ZncyJb?)q>x*g!QFo2uF3pOf2i*c%xiF%q8;Mq=t+XM-42ggvtZpKslcX?;t~RI2w85y#42Rbsf7Y+@6YMB%THs91Y8w|OIjY0QI3x>NF}e#L_2~U(k5SW=A~1266sI|H1Qy0YD0UxOHFd=Ek4l`&L|#%3xKNN}&^<k5XdrWB#QXH>0N69h)g0I#el>F|;^)GJq6pO&lk}p55MU0LAyUc;m4UapTc&>CrKaJ~j%gm>3MJh=87B-*D?YK+NYC+SD{9D8s#F&I4_cH5KLXUjwLnv{J1aqyHGN>TOzkCeN-6T^fWS*~)KtmC;VgACPr1pe#4BNfzeI$zjYh}dy<;|KJ%DG4y88aVT|}(}3r>L}L)z<VJ{4DsijQA?<tBd>z{sY!@iu=8;b~ddsUCgJufa3vYlXsc+Ok`8OB*Djolyj<#VPVjn@a&w<d|{hgm@kdnB_urs~baIrh*1(JwNY_SSoU?3W3|9oZ9+k3oa!)qN=ZG)vsM8iLwe+_oxW5Nm*6Dc+c2cqJYW^2wYbh2~8~}r`3+^GNKZGsggP=h<le1ALq|u+*;jOi6bm^Q=-{D&1|4o>9FpWY!}F9T6Kvq1V5HQl|}n1fj<beP*4EN8rUvz3RS_8BL)PXW-Ir8C%)*H2nqQF%ja;J5b-w1T&n+4^ic%Ef!6M6255N8B{qRh;6w6@hrL*)@9yq>plE@0CcrHP%nxvd<2p;CG&LuRIcApNm4niLg{_2^f_a3%y8t`SR3VIjE2qt!7}}|yvo{#2hR+Z=;79Mx|5`#b;0ib(nx=voy#*oN?F)KUS|m|OdIe&LSC-J2+*n_U64ue|^2t9-G`-`UpO75a$&c1v9YiUAW!Fv4+i#7wx$ESTX_q+#v9;7#fCw+m9LVf$q@v4USO^FBlsN7T@zSP2ux7#jVv5XIk=)YT2L48qlO^2fT$+@X&HB>V^>Waj7m^E&)#4Z~qT)1O<1iM#aof%EE+6gg?PLAF+1b=+te66cwAo**BdqK*sQaPoKrL&xIc=;2(#rh`=19L4oq@S2RMu`1UlA}LYtK}Ny9fiHHia(f3zU$em|U%aUk;=T<Z%Gm*tR(x#qj${6bU4EfhS>JI{9VayQB2XHf8$ICZkKRI9P2WXEfw}>a3HovQbGK98H=EfN`+U?OScsn3lBR*wHTN1|oAytH|WI{B$DigqtwkIa9(i=Ky-_j-W)mh~a_$yA}b<P{w5tZ#3$>J3Js3C!I@;WWjS=7DHP&jXp#<F!S<RSwjKZXmdjRHbM`&6i_O$U#G>OWpv8xpDMH{J>6Ls6};{%0awIZZCQ*(goFH6bq!dl3N3UvQd*2jw?B5+tIHuemt{#@p8zdUok~mWZe0$YL?kgL&aRfWdrhuUlB4s>n_e87QD%sSl={S_GsUM5+dR`|*HbVLw3O>K!%qgsdHGGn?C%_I6?t0#c^Rt8wf(N2O{<4!LT^#CRAhNGM{hMUGn4UDh6%)vY_#~a1+`+f^0gk1z&OBWuQAv3-hNe@HHf7u)IRqZ%W8Xt)^XHhRr`!f#87C%!#3i`Av6v5&2gAV<0M8zQu+HEHI#?EtTa{t;}I;72kq6gV9~Wk5vcEtYGMPn7t2Ul{FA^NG&+mp0ekH*FmOW6O{G&>1P%G6G?XPOEu)4~eh_woPN=VR>6A^ai(HgJAcG+$hx0pQ;4B?jKU8=tY8r$Gay*y}&dm<k35%ZoN6F*z%E9LNc4fPJZ~z|?xtLD(d6Da(BOg1?7>JVN?PG?wQZJOH49Iz2(`{%9L1~~@rvgM;P->`p#1TCX;rk+IO@y_~HL49nN|y*{R;*aXj1+QMsnl}?bx1y>HjltU%<6D3m92y_&0ssL+Zsr8GLhrbtvfZ`)Fpy@L^6(Zh^{I+R8v1{?{K~5ykURrXiza)@+_8&`v^&LB6F5HEL8n?(UbS1r<at4pd?DvFR5|3?VLWrt{CGD=|QXKJSJjeZ=o1;#R10OF$!-lT{pfoN?`lPdWQH*4bs1|gY`n=N1tM7-gtpS9`YRX4~&*|t|G(V&+}$!LyjLJt;reSQ(geYaIfJ3{`mhJcdrc')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
