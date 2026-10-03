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

# Locally implemented, observation-reactive executor of public production intents.


# Historical episodes supply task targets, not hidden live opponent observations.


import copy


_ITEMS=('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL','FERTILIZER')


_SEEDS={'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}


_ANIMALS={'COW':400,'SHEEP':500,'GOOSE':300}


_HOME=((4,4),(5,4),(4,5),(5,5))


_STATE={}


_REPORT={'errors':0,'seed_waits':0,'supply_waits':0,'weed_repairs':0}


def _walk(position,target):


    x,y=position;u,v=target


    if x!=u:return ['EAST' if u>x else 'WEST']


    if y!=v:return ['SOUTH' if v>y else 'NORTH']


    return None


def _fib(n):


    a=b=1


    for _ in range(n):a,b=b,a+b


    return a


def _tile(tiles,p):return tiles[p[1]][p[0]]


def _home(p):return min(_HOME,key=lambda h:(abs(p[0]-h[0])+abs(p[1]-h[1]),h))


def _command(obs,actor,tasks,state,needs,seeds,stock,claimed):


    seat=int(obs['player']);day=int(obs['step'])//24;hour=int(obs['step'])%24


    farm=obs['farms'][seat];tiles=farm['tiles'];positions=[farm['farmer']]+farm['hands']


    pos=positions[actor];inv=obs['private']['inventories'][actor]


    pointer=state['pointers'][actor]


    if day==29 and sum(inv.values()) and hour>=21-abs(pos[0]-_home(pos)[0])-abs(pos[1]-_home(pos)[1]):


        return _walk(pos,_home(pos)) or ['DROP']


    while pointer<len(tasks):


        task=tasks[pointer];target=tuple(task['xy']);cmd=list(task['op']);op=cmd[0]


        tile=_tile(tiles,target);distance=abs(pos[0]-target[0])+abs(pos[1]-target[1])


        skip=False;replacement=None


        if hour<task['hour']:


            return _walk(pos,target) or ['PASS']


        if op=='PICKUP':

            item=cmd[1];quantity=int(cmd[2]) if len(cmd)>2 else 1

            # A historical pickup is additive, not a target carried-inventory level.

            key=(actor,pointer)

            outstanding=state.setdefault('pickup_remaining',{}).get(key,quantity)

            skip=outstanding<=0

            if outstanding:needs[item]=max(needs.get(item,0),outstanding-stock.get(item,0))

            if not skip and not distance:

                take=min(outstanding,stock.get(item,0))

                if take<=0:

                    _REPORT['supply_waits']+=1

                    return ['PASS']

                stock[item]-=take

                if take==outstanding:

                    state['pickup_remaining'].pop(key,None)

                    state['pointers'][actor]=pointer+1

                else:

                    state['pickup_remaining'][key]=outstanding-take

                return ['PICKUP',item,take]

        elif op=='PLANT':


            crop=cmd[1]


            if tile=='LOCKED':needs['land']=max(needs.get('land',0),task['quadrant'])


            elif isinstance(tile,dict) and tile.get('kind')=='WEED':replacement=['DIG']


            elif tile is not None:skip=True


            elif seeds.get(crop,0)<=0:


                needs['seed:'+crop]=needs.get('seed:'+crop,0)+1


                if not distance:_REPORT['seed_waits']+=1;return ['PASS']


        elif op in ('BUILD_PASTURE','BUILD_COOP'):


            if isinstance(tile,dict) and tile.get('kind')=='WEED':replacement=['DIG']


            elif tile is not None:skip=tile!='LOCKED'


            if tile=='LOCKED':needs['land']=max(needs.get('land',0),task['quadrant'])


        elif op=='DIG':skip=tile is None or isinstance(tile,dict) and 'animal' in tile


        elif op=='WATER':skip=not isinstance(tile,dict) or tile.get('kind')!='PLANT' or bool(tile.get('watered_today'))


        elif op=='CARE':skip=not isinstance(tile,dict) or 'animal' not in tile or bool(tile.get('cared_today'))


        elif op=='FEED':


            skip=not isinstance(tile,dict) or 'animal' not in tile or bool(tile.get('fed_today'))


            if not skip and not inv.get('WHEAT',0):needs['WHEAT']=max(1,needs.get('WHEAT',0));return _walk(pos,_home(pos)) or (['PICKUP','WHEAT',1] if stock.get('WHEAT',0) else ['PASS'])


        elif op=='COLLECT_FERTILIZER':skip=not isinstance(tile,dict) or not tile.get('fertilizer_available')


        elif op=='FERTILIZE':


            skip=not isinstance(tile,dict) or tile.get('kind')!='PLANT' or tile.get('fertilized_until_day',-1)>=day+2


            if not skip and not inv.get('FERTILIZER',0):needs['FERTILIZER']=max(1,needs.get('FERTILIZER',0));return _walk(pos,_home(pos)) or (['PICKUP','FERTILIZER',1] if stock.get('FERTILIZER',0) else ['PASS'])


        elif op=='HARVEST':


            skip=not isinstance(tile,dict) or int(tile.get('yield_units',0))<=0


            if skip and isinstance(tile,dict) and tile.get('crop') in ('WHEAT','CARROT','MELON') and not tile.get('watered_today'):


                crop=tile['crop'];age=day-int(tile['planted_day']);low,high={'WHEAT':(2,4),'CARROT':(2,3),'MELON':(10,12)}[crop]


                if low<=age<=high:skip=False;replacement=['WATER']


        elif op=='PLACE' and cmd[1] in _ANIMALS:


            if isinstance(tile,dict) and 'animal' in tile:skip=True


            elif not inv.get(cmd[1],0):


                item=cmd[1];needs[item]=max(1,needs.get(item,0));return _walk(pos,_home(pos)) or (['PICKUP',item,1] if stock.get(item,0) else ['PASS'])


            elif tile is None:replacement=['BUILD_COOP' if cmd[1]=='GOOSE' else 'BUILD_PASTURE']


            elif isinstance(tile,dict) and tile.get('kind')=='WEED':replacement=['DIG']


        elif op in ('DROP','PLACE'):skip=not sum(inv.values())


        else:skip=True


        if skip:


            pointer+=1;state['pointers'][actor]=pointer;continue


        if tile=='LOCKED' and op not in ('DROP','PICKUP','PLACE'):


            return _walk(pos,target) or ['PASS']


        if distance:return _walk(pos,target)


        if replacement:


            if replacement[0]=='DIG':_REPORT['weed_repairs']+=1


            return replacement


        if op=='PLANT':seeds[cmd[1]]=max(0,seeds.get(cmd[1],0)-1)


        state['pointers'][actor]=pointer+1


        claimed.add((target,op))


        return cmd


    if sum(inv.values()):return _walk(pos,_home(pos)) or ['DROP']


    return ['PASS']


def _project_stock(obs,commands):


    stock=dict(obs['private']['shed']);seat=int(obs['player'])


    farm=obs['farms'][seat];positions=[farm['farmer']]+farm['hands']


    for i,c in enumerate(commands):


        pos=tuple(positions[i]);inv=obs['private']['inventories'][i]


        if pos not in _HOME or not c:continue


        if c[0]=='PICKUP':


            q=int(c[2]) if len(c)>2 else 1


            stock[c[1]]=max(0,int(stock.get(c[1],0))-q)


        elif c[0]=='DROP':


            for item,q in inv.items():


                take=min(q,max(0,100-sum(stock.values())))


                stock[item]=stock.get(item,0)+take


        elif c[0]=='PLACE' and c[1] not in _ANIMALS:


            q=min(int(c[2]) if len(c)>2 else 1,inv.get(c[1],0),max(0,100-sum(stock.values())))


            stock[c[1]]=stock.get(c[1],0)+q


    return stock





def _market(obs,commands,needs,target_hands):


    seat=int(obs['player']);step=int(obs['step']);day=step//24


    farm=obs['farms'][seat];prices=obs['market']['prices'];stock=_project_stock(obs,commands)


    animals=sum(isinstance(t,dict) and 'animal' in t for row in farm['tiles'] for t in row)


    reserve={'WHEAT':max(3,animals,needs.get('keep:WHEAT',0)),'FERTILIZER':max(3,needs.get('FERTILIZER',0),needs.get('keep:FERTILIZER',0))}


    if day==29:reserve={'WHEAT':0,'FERTILIZER':0}


    orders=[];cash=float(farm['money'])


    for item in sorted(_ITEMS,key=lambda p:-int(prices.get(p,0))*stock.get(p,0)):


        q=max(0,int(stock.get(item,0))-reserve.get(item,0))


        if q:orders.append(['SELL',item,q]);cash+=q*max(1,int(prices.get(item,1))*.55)


    count=len(farm['hands']);hired=int(farm['hires_today'])


    while count<target_hands and len(orders)<10:


        cost=_fib(hired)


        if cash<cost:break


        orders.append(['HIRE']);cash-=cost;count+=1;hired+=1


    owned=len(farm['unlocked_quadrants']);wanted=int(needs.get('land',owned))


    if wanted>owned and owned<4 and len(orders)<10:


        cost=(1000,2000,4000)[owned-1]


        if cash>=cost+20:orders.append(['BUY_LAND']);cash-=cost


    for item in ('WHEAT','COW','SHEEP','GOOSE','FERTILIZER'):


        q=max(0,int(needs.get(item,0)))


        if not q or len(orders)>=10:continue


        cost=_ANIMALS[item] if item in _ANIMALS else int(prices[item])+12


        q=min(q,max(0,int(cash//cost)))


        if q:orders.append(['BUY_ANIMAL' if item in _ANIMALS else 'BUY_PRODUCT',item,q]);cash-=q*cost


    for crop in ('WHEAT','MELON','STRAWBERRY','CARROT','TOMATO'):


        q=max(0,int(needs.get('seed:'+crop,0)))


        if not q or len(orders)>=10:continue


        q=min(q,max(0,int(cash//_SEEDS[crop])))


        if q:orders.append(['BUY_SEED',crop,q]);cash-=q*_SEEDS[crop]


    return orders[:10]





def intent_agent(observation,configuration=None):


    step=int(observation['step']);day=step//24;seat=int(observation['player'])


    farm=observation['farms'][seat];count=len(farm['hands'])+1


    state=_STATE.get(seat)


    if state is None or step==0 or state['day']!=day:


        state=_STATE[seat]={'day':day,'pointers':[0]*30}


    if step==0:


        for key in _REPORT:_REPORT[key]=0


    daily=_PLAN[day];needs={};claimed=set()


    seeds=dict(observation['private']['seeds']);stock=dict(observation['private']['shed'])


    tasks=daily['tasks'];commands=[]


    for actor in range(count):


        commands.append(_command(observation,actor,tasks[actor] if actor<len(tasks) else [],


                                 state,needs,seeds,stock,claimed))


    # Prefund imminent seed tasks rather than waiting at an empty field.


    seed_need={}


    for queue in tasks:


        for task in queue:


            c=task['op']


            if c[0]=='PLANT' and step%24<=task['hour']<=step%24+3:


                seed_need[c[1]]=seed_need.get(c[1],0)+1


    for crop,q in seed_need.items():


        needs['seed:'+crop]=max(needs.get('seed:'+crop,0),q-seeds.get(crop,0))


    # Buy upcoming task inputs before the unit reaches the pickup deadline.
    # Only our own demonstrated task plan is used; no opponent private information.
    next_inputs={}
    hour=step%24
    for actor,queue in enumerate(tasks):
        pointer=state['pointers'][actor]
        for task in queue[pointer:]:
            if task['hour']>hour+_INPUT_LOOK:break
            command=task['op']
            if command[0]=='PICKUP':
                item=command[1]
                quantity=int(command[2]) if len(command)>2 else 1
                next_inputs[item]=next_inputs.get(item,0)+quantity
            if command[0] in ('PLANT','BUILD_PASTURE','BUILD_COOP'):
                tile=_tile(farm['tiles'],task['xy'])
                if tile=='LOCKED':needs['land']=max(needs.get('land',0),task['quadrant'])
    upcoming_stock=_project_stock(observation,commands)
    for item,quantity in next_inputs.items():
        needs[item]=max(needs.get(item,0),quantity-upcoming_stock.get(item,0))
        needs['keep:'+item]=quantity
    orders=_market(observation,commands,needs,sum(h <= step%24+0 for h in daily['hire_hours']))


    return {'farmer':commands[0],'hands':commands[1:],'market':orders}


intent_agent.telemetry=_REPORT


agent=intent_agent





import base64,json,zlib


_INPUT_LOOK=1

_PLAN=json.loads(zlib.decompress(base64.b85decode('c-rlqTaP5kai#xDKlg**FM4YZTjD@N_Mm6D11-@Y2xtK=7Lax+3D||8|Gq;K!^w-A**WHsRasRDKJbDuW>ls}guB@}-}&8tzWd`J{^g(l?cLv%_wWArKmYVUe*edR{f|HW_+Nh)-~Z)bU*5m__dopG|N8U)^1J_h_kaK2kN;lYmmmMvfBoM-{>OLUe*M)y{`T8<@85m(>4$fJ`KSL}|L*VN`*;86KmPE~fBM6}{QHmp<-gu9N`LX&ufO@_@4x-<-S@x!{PEr2DwAFL?KdC3`gr}B8L0f}a)0>M#}D7Xd!PSST<qe%|M>BjKVN5E7i6)ZuM3h`Fzte`KAe7aF{~@%`FHo5AOG-ozyA2mr{A2ECcE^958r?Md{QEO-(m4-fBm|D{*8lOdhu!LVnuy<|I>1;tKav#Uw!=e?djq;`}@+#@0+a!S*4YcuNLIhr#8Fx{3q=E8jjY2DfEIly}t7`DXo+IKAB6b+NGCEtVy>(vX)pJcIoA(O=*dh_my2@d3nDIORU*<y12x;bmM082MKoR<yRD?68q=RcIoA(73nb%&7Z&9rI(*Jq>|)+o+Z!oteUUav!zx}?%QN7wISW{$$GttPnT%^^wBQ8{4vDmjQwfFF1`G;D&2tYg_ih*mfi>NLOU&m7h2(8oa=p#u+)lODL&PJ-PQT4tVvH7`xnf1DfnQD_AeNlU3&Rx;<L>Dv}u=Ku9u4?_T|f;tAs<skN-dK|N8%>9TL9!^vyRPzxw|7fB*6G_g{bW^?yJ8xM1&De);*+x9^yf#reue{FW*)XNvO;Qn8<}(6QjO;Qa3ap5WRSKJoL_N%`r~F7515FK?aG$5Dp<fV}$$)Sc^Z?6FV$xq|s314@l8?9Z2Hep-rl>E)v$Nx!B1oG!qjR{8PU?vForo(9LAm*i8weCEmC1(TEwy|`d9zoC#j6Ugga`PKW4e)SA|rww{uA#a?p_%!%^on7ziwtio~?sxXHb>@`zRZMotuReVKZy&$=-q&IK?)%Rle)z@5&!7JZIX@TlBy_sm6Zc3*HzYuR?FP?=wDU%YH}0UpKgx@F&%WT7MB*D%rzO{Sbv^8jqO>&lw#4L*!AfgEEUI(|WAZ2FXqR07E{Q%X%MaLq|Nh!>e)&{y{B;7|(5vf|4g{<2>*_jFqFb;jOAAVwLshzq-RVyBr2D(_yPNJpM(tOM9dCRsSJU8c`+1Wcr#zbtY%?&ilheZP0FT;ZD*J>$pUmW5boR`==*@Y)%?7dUZ4k%q2J!Nj5Vl{+C6wK*N#pmZh1nQ^Ei0*qDZOu3b6VzAp=`b6R|UGot-C+UfNmY-3gYe+B(`_l_+eGBORir^5uc|m*F&VQQ|?77?b1fKJO{mdjljr`_yWN_V&bne<1?-0M^=8DF80;}y?HyWxcWK=-jG}UX?#;I@`3>Q_>nvvqO{o|O6)FG({AO%M~d>>?&WM2H+wPk$O+x8%<T<RWOp1f(c9xf=>f0K6w%fLf}7a9x7$dp5->f{t~b)Vz;@tSBGT{dNWQa)#ujpT&wN*=I=UT$*X#vecz0xv`nh()kG90Ky=e$B2|qu{d|#yA=v^UwEt&0*+|An|aT8C!YKVV6q}@x%dvEZ#eF5^GB|p_zZt$<@_~H)Mw5m9IUed~er_l$-!JoqdKd#Jtf4C|y)gixB#TTn`N{_6p#9{dAj5_)J5!l$*{qq^V(D%LEX3FduB3{2gl{EPsKi6;ECJ)HNx}u6-_IXnx2@T|{MVi?~%CzoLb5FI!_tXA9MDcwDzD)U=W3+!f;iAu9kn2+Us_VMAvu3e%sX93Oxnuxtp=g(?-R%VKV57Z*P253(o-Cjn(tf*x1YlN<(rxBmv30RxFF&<z-DO=`M7F~^+NI)MmXck3@n{wwv`bs1zIOA@>8r4<y(bzZHviHEUJ%mqV;=I?KT6tKyjgnQnv3_m$+#|+UlH9dzSxNjyW(O`ChlFt8zkD_C4NigyHzAas%<1Lo+<4n?X{EapGICg*)G;b6vjPrd3QFc)^zyBX_pGmgv(v@X@f%CoA7qqMmPP3^qbr6PH{I1b_q`JdHd6fU8<grPG6{`_jp~ZdXIlDnf9kiN35xcGNQbmjyz)tZ{Q9XWW_fTDEdA9)=Bg4x>VKloqp@2`FCBanu*fg3vlmlhPPqoPQ0x%p|{?qr0$+|j=-)Wld?s5PIIjHncMfsZ8URBAU(R<VoPv+;){0iMQbhD6~>14w9P#AHZ#sB^Js-G{xY@)oNqC~{XnvVo~iM|I^ZfO_E~pXE^gGib-L|HyG<FB373dc4fK93Ks7+_IdON8yql(pI^|AFvUk%oQ6t1@N%3!*3cqQhbx&{2P>^XbU7{6)()yQndsY67%DxHZ2T22e>03P)I{5ix_w!@CMW=88t@&Y>%H5u67wZ$qd$NN(Z%?qwx1hK$4c<;mL(gi^dH8Y}2pa+PNA=u4$?oRC!wJvl4}K$+tvyBuh2T)XJ=+5*>@hBnu;jiCxCpxaG`Tov#N!$<icqQ3LM4Y2I`aDC%&VL$FJ<Z5h*(D>=5!0NbqhBSAO(K{q^(I|rr!V9GoaCTbffQRMUymGO_Kcbc#3HXueB_^*3v<6t-!loeCGsKj#GiTMzl*|IgTQOtIuNSiIgi#xs8h=1l{e>T}^-j{>T3M>u>(?-TOxEqQ#RfZ9^-EDgE=F06h7<{7PGhU#2l^8_#I{PTUmm#BBwSY<+Vy4C#f6yj1gEdvg02(RaE4q6jB@B_ADX0%W@wYgBi-Q7s=0ki*2qX8@fL_5PShYlD8OW)`BHS#(_5K|Vs%<#bz5HAh`WjdGqttLvI4m2q&5+g+y|G;G}<#{lHqfWD0nY_2H%kx2JP(q01?>961~S4=h(c;QNtA5rPf-5edKMXs$0v{W|jNM#c(l}+>k`T4u6$a^ibQ|Y?b%kAv=X|gln2na=RLmAXo$#h$#?DfNt_Ah2fQ#=n39o;cHI<2of4h)e~oL-G~YYn^N>N)SXlS%jNKwI*da5&o~*DtT)*EU!F5*_N=VV7M0Rnsj1PJzBeO+)>5yU2|f)N302&a1$uU2=_74t5dQrS6_RG2f+5^h+qwFCk3;?Ep6vp4z8@jsLuO^(ME_=H4S7{Iq@j;nSyY#J%TXVYiuMA2@PM^KJMvh+ynu8yPnn-N}|?^YSrtN}0BF2MvXLuS?+PTJulens551%#;#))_+O1;48ezaT?9S4vHXMpLoAkuBD%srC>{cU97eA*A-ez|1=1=aq8oBsoE?%Evb+_BU>;DE!jOWj`QTV!)Et~Zg_Bo$91-ssPHT1#R^qj`KP7!+DUe)dZ;@s>D>8jU8<hXPD=)-2w9h^FS65;$-R@-rRqB=gOH12K`tI6vLCnj)w}XfOTm>Nf%~l5rQphsz<oCCQgG!*`#zIaew6Ps?QKG@{1-IjlUv%fP;hQGv;!?uNVH4=kV2@}Sm<$5qsK|W$V$D&LEGA-)5}CNt{(k7Q*0@lKLgtdZhR-$HFH)8f`vVY_GiKQJB6dyCoYkCUAY1F`e*|Vu-C<!OzO0vd*7Q$eoM>m&8KmAn7b-r7ZH?ARgg;DhnK(~Uc%z%`u@|eKYahm-opj{^b!`ks;iG1b}hJx3yb5+<;O{@F?h}|Tf4Z9aSjk2Q`?g<b#~}a&-~>%Y}wLI3|c!eXzj$<)J|-A@xdPS)MhF2R?H*}NW2o|uab9hm@Dcy{Wb)(6bf!B_-?E?YV0Z0r(Ld%j1uDiN4&Vuu?batK?p(JP0@LUTNQW3Pdh@6v<)?SY^agv<wxFzO7p-X&jSmnjKr75d^QeG_BdP|i680w$`9w)(>cGc6%1i>iXQo{L!nz65eN-~`ma#yB~H670-YnFj*1+73O?fL-~@IjlJ|BZh3&s~w*NZz`md92zec+Knl{_7nLb-o`fSlQ&lcU*vHq=&3t|BMC8yfb#V5(=dq=Z(Yb+>h4-zYH0Q3;>&AFa*D@w9;fubZ63Q#2(qK=4x?i)s+0#=fp)(?)2w=Pw;o2MnyuTGh)Iwc})tYp`!_Z!;AsxN*R*)drc(r25ScELcqYv@FgZA)U|TT&u~vT{4fvMg11kmckLtlSQAU8?RN3pR-;^pU;U6<5cL&d$m_faXe}C-fL<09H{qVHM5J=7roRP^_=)nA$vD<PA;**5}*=TO{suA@=|W4Gj&nPCRbv#1pN~D6~4GZmKgHZ|fO$3GD9b{)CL~Nyvy=m#nhS#kuuZ3|j&Kv8U0vbhW%J1@i#c#hT=3U7<;iPAdktSk|TLVmTL??u6|e@Y;=A>nm-oFOlO+3QWqf6cm`Oi#0;Rx<Vr)oE}Kr8^Pw;2zsPx>6sp1u-7C4_$a`WFE0>a$E!U~T%N@(7kqN;-qXg24jv~&zy|NY%qAWHOF*)J{qdVmzd1t_Dm<i3nsbCktB`nd^4dw>n=BvU55;!_;aS&fa6D(?7NQ_dcFDCoCOaniyzIE!6<3!w=-o!%+HC->3yuF0!7hHXn(~<q0m^I$P~HmxdI3rG8Xu<fiigPSDpZj~L_`u~d{wu#5}8Y#DOfk=z(k3}at0F18Q6j<XP!in)mKWki+*~geE0q54?q0k<LA%+v?qDE8zItalIpn6Tr!9L3S<rixmS?UQ{Njs4I1qhXtZ10biyUN*IMXaYu)U%wx<Uxvb|P>=W&SAp}#7n13b7zbO?i$Apq!zm3$`B#0goi(A7^Wv`0#|T6b37pt-Z>6Pcd7r8AIQhl%YRW}pCF?WcYov+vmLO3iqRc!y-eb0J?Wu&N=^s)j<V8tSI1q0t(@L2LZxp2kmB-c{_yQn1E_xZlpV_vLD5w?xIc{8ao8pFVx}@wBr%ZHL8Q8`@ueLi#3Y(apa4Oh?<~u>N;M_kY9w-AU!OvdC_BBzg1N2(%qO>2`Po!k(^=@5vo5B^$t=f_G5WrUWn=xP3rZ!^yX+lIuRV0%gFqKG}u|Eq1q+Mi4dHUq5({JmAQ`UKkO#@n1RJZ{y<!&jo>(Ju9Ag`CKqjg$AOK7A4Dy9JSd3R$bIVWugySE<1Ufc;qwXff#xiNsh$cSN;-tc)YwRk2`)A*e^fOS;u*gC(yBn%0s+8h5jhrAX|ygsO#X=5pjv7u;&t!#faEs_1SX1vd2Av%sB@;=bW2kPEr3-ID*c)6wc`=Y9o)Q5J^YDU^wo=fg{`mk8lw^6aYCm;IS4qy#kR37<3zxV7f3Ny29m;i%krwJpgFP(*{xZ0s>-3%RlQ4`9V{BCr{#yJWe;$Ok5ceJeB=fb7OmB=Pz+cKk@YIx9QV?Ci%WR9XJ>qi4>SrOJI_*p*iwG-^{2i><hiIFZ6Cd=Rs*yrlnDN>meUOZWz><Et`#5Al_^BRvEnNYuX}~)lMTLy<9!OMaMJ!HNd6aIC+rtDOc8~T#th$KN!d_h=DwC3@((R=97z5MlPbfnGk)+O9f-dijql#Ey5<)A|A%&4|?}qZU|SN=i1oaV$^r^G6SRWPQNXV#og;m8kR<Zs2#_i+HpQ#GWXMnO7#1w(-a8=b79^b5FJBuHY)Q7?RA50?>HD?+R5jmF%&d~ViQ6^!w4rG&v!GhU_uA|SfBy#k&4ak$`Oa5#FGe<PoAGV^85y8@~ux9N+ut6YDzYHX(P!64RTf_=m5L}mZUTqMcfWV5npt##jme%MDDUIC3J$=o`la&D|UtMeWwE68hw48)^<-`qYXq~7|WN6+K^5N+9eiVMh+x)8Hy@B<_nF8*v$C?JJ5mXK%YF><t>^m>DF%yUZUOXt+DPr<`vgGc~su=C)7Q-E|PAR!e3&gW#pZfk&jJOETAtk_cd6~gD>ML@5um)Jzz(fJ<3pi*szh+HZ<^z5`aB#2(_TuzdU7tWw4MJRoaP16!Q>4Y0YcE)AMvk1vVtl%Jeys1N4%4oJ_Sf5b*MgDAo>ggZr!s#XhHHcHWfPc~jnb`&TR-0kJB~%_JAzQY+7!BKz|0JR_%j7&+a~$mt$NPPi3#{iTYFihY0@b|rQwJe92w&SFLFB1f1H_H1`ra=m=3KZ(5Ym)LnoyMweIZ%s?Th^iMSKql6++Lb@G)h|9%<TY}ueqE`p`qPTRq3G77>dHSYncNv~U8=q&PTOmw$ZlN<PKFu_NnMv3)1h0WR>|*;yHL!b*5>TV0z_1HomJV5z4P+4rSIko3RBD{T5DHmtzETG9_GjvJFo!qy6cfm;05*vWY4{sRI3N>X&d*X2<j>=sB4>ox^5rhh*Yb-=K{o{cJ3wG>WwP+-axcf<|l92GkMFvJaO=sIBCbaFPN&l0$|j=2UEQSg}5tTJ$n$>*^ju+eETkW;ua_B<m3&^k=5NLR(F@#IZkEgICqf~?D04kV@KrB=84H5bOXKe4fMkH!lCqIIm7GV;m;$(>*k!QJxw4cCWqyHnV(NpyTtJKu8W}7BX)_yMo5uiUJhVY_sppjlT5K~HK^<`+Ca}nn|OEx>$EG3teAC?sJ4qdB{uP(++vr&v#DeYMCCN##?Gcr56S1MUfG)D(F0;@95SFZyFyo>P&uoEzCJP2m30)2El1IAOuVsRA;Dmy1%rK4FbE*bD8XRy2nP8?wB$(XOPX+F(g>PHOQ+;~G1Oj^Y!<79V1x*+ZI8S#HlYZBk`lHkY4Xd=^O{5@W#s{j6>UVUi^wo~<q|KAxLC_NzXDOvprt+2C+(U1_KD^PB@aI+`T0SK=LZE|r{l6<RDRvA^)|}7T^A_pRwzK%ZCQew%#IMod&;~NtI;kS*~>G~-05|ZIKB(pPN36gVdgo>YxVZxM{Bg^yVC~S=?Ec=!7d_`M>Pv@;=R0u5A<rbPr-O4AC>}U?GfLeO6yL!W@TsVn?Q94#6^pnTr|f{xgMA@Sv(r5^2HUKSDw80f9E<Xc{tJ7;Y8mXPCR1s-h6DH;<lCBMGqC#Lq)X_s?qpR4W2;YA)BSQDTLZQ3RgW_@h0vTv+;A7vqe4XU>=i38%1PWO847RI&4dM5XeX+RA-e?gH=L7%rWSU0&Ag?hf<b#B~-Obj8^Kp2x_HbmpCM`R`87IDh{kYeFfz$R@wQj*z7|Jwn_lG5{kB|hR7})mZ;bHguAY;#%dQqx(MtNJ8z_)yh}aVB@{ZjLxHH!WT@H|dceuL21yNuu5a)oC?K%`4#Qg|M4(}Kg&$D7&X^6wG%p=3R9}CJZeM@m(E~@4(V8|T&vuRQR~5TbyX_&RR%e|blLjS+P3uRbtsj}Tew0n?#|y@;4a3M0WsPfr^nYt_HY%b5!qXb<1n;a7e9}JfuqiK!ydfNbUcsQYxWE%$y&)@qjqNaCmJa5c4rm?XbT_R|n+Ew!ksUhzFGs2El+pjND^P`F24I<i=h4N(z;cN{y(iR^bl4Q1Sn$EO-~+$lyLM^^4F70SvO>B}Ht8B{Sav|>KkQQVw>=e~+bHg6m#W9w@@C*`PnGPbp{^4za4U8R;ZhlXmkLc#i#$OsdX$;-iItf$1*WnTn6^iO>2yR*piL`r)3lOklZNcGuk7=Bs`B=37m*Kn?GmR{f*a-!li}s9nb!I1HS?3K!VIQB$9-WP_l{faX~$IAm<BkqZ9GP%*zH|3d_FrZ`sLUEV2kdOeKJV=HeVLrWjGKAxi`wrl=s<Yu$6Yc*DdG!y{gyrj32=7PN2iu9y$y*t{)qiTfV&Mz}(7aQ&l!$w{9lvHkzN*Xns<=UBYgsMWSO92*{_#$PM(O?mlU2zg+;{VMg(Hzxw#`+f%M{VP&k9m9aLqr!d%_!rbdANYiOW!xytH`!m}0>mq^M9V>+2{>#(*>L-qnvQfS_*A?2mxfTwZ-AG7pD5uS72mkhRWUQ6-jCR&DI`)LJ(@qE^1gs4OzpSODW+XMHNNv2jcF^itNxWJ$y-12~K7HZ^z*?4Lh9pkwffNo#H#vwmflWYQz67U_LN2?o>9UJ75k1qB@Ul4xuO84ww~NmD3lYdu6X)QQ_9`MA_Uqd?@$mM1WU_CA??z<q)^C%^R8iyhx&#hztbla2@RxWT!m@fYpsGIus`437jTtm!6u&GJoKTS-a@uPAX)D=!*)7vsrcG~|HofI-bodr;Z?#i94x1Oz5&S0iMUi7>TfnJ5c-J+^HVBf7wtE1D8~BgoB&N!sG}D99;)pnwb){vib3M);71#F^&qtKUmxcFF6rX<rK_Vm;9#U9%NZo^nG!`B*Sa`_XgNMjxj)EF7B4X6ev{Ack8npq+t{L3~A$AdP-fBA(cxaxeiYXp#>K0oHwN+Ldt8VGDAQ=0kS?uyE4!q%0(|;BZ`U&7gogaAtm8p2-eHPBt6GV?CHrcDNny$L1>1wPSX3}PuuxW;gv>7JTW|*>RhN*TCiutU^B3=d`gaSma7(L!~5!B<|&T2tMhKY_bu670PXf=mr9SUe(&&q&^X5|iD7if1VmU@+VHFB{_2x)QmON%=n&OBLbYQhI76qh#f=-jK$!2_>&CwN8D9;gm`?uV(kmw#(K0-zC5+Z+*f9u_(6SqcSlOb>|TQ$rjZyXS56p0{o8c@-IJre&;!P0EUmmg53(Xy73&d)$BzZsLQRXzW<EzFM)liDtVS!z}{yAoKNsjgcVaqAnj@3&_r;+Kmybf#^9z8dq3pT-}q#HGZ@a=<KINPlxj6phxV7G`yby*@F>lo4N8KN1SFven1zW3%UrOV+!aJf-G=}hdUG=PSSZe$#lR;Qm~88&2P~z5Yt5x{YPm%bPr<DF*V}lVAX+HY<s@2!6%yXv7~a2dEg0+!9!>Sra_Ir#%@y`342^W)*h#D-5YoVK$@pwSD;z283;~o^aXZWTs1wZsllI`8hQCwqEYFxG{8Z<nEat)@<C7@iXpa6*A@CYUDqHyH|Y90&D5Dv1?z6?o9@P^4qAnkz`I;QWhRQuDpzL+McZ3;lqpe9?x{3iusLFd1|1JH`Iyh>iTO<an9ocrmgF7|9hVW&Q!JRmE(c~*jzIx6v*gCl^D+Wa85h8xXJlMEd4ZseOOF^#{)oZMUt-}ogUv26TR@mRZQ3Ouye0VIE#cUKTX_W%u%{H^d#qWVrcHDj1Jh{?Oy9)7DC`G$Zw0fF)<saXjSEk4y!h+Y5F%v-*I*S~h~&$Gn<$2>J<&l8G4m-1m5&(cHoxEO25lu1q}>VJ>kII%*m6hE9up{lm-}XL*+8ZG>mtbNi(R6FG12W3<AA>|f~>yKB_io+6vd^(oQWrpN!Eu<^1f533FlcRhmEkzGTXdK6FGy?=o>%d9KP`C#D`bsx2bz<*bRo96Q57_=sBtFbj}UX*>Q<H(~gso8`_0;?9^j1`}LuLd}tugPb(A?V{2SVSduqE{pRooJ%!a5A3fc4U0tIy;yMlem@M=|j%+I=1{&@-itiW#9)pFkI3$xmev2_|dd|=ndb5Uz9}_En%&hpavf{_a>KF$rW1O3L(}B-rPBa!F7P|!Yd=&sE*7!^8Ji1}JLKH5?PiuZ2JcQ+qMP*N-*l39&AZpaPmFpTPwGGoyKBLvD(^jiaTdmY^vs>}YHT`5fFkT?5`U-%lhh(%vhWKGu=<9r41Fdt+u^)Lmd_GLs7<kitP`LnucRmHX1a|6252#Nu1r^&ygeoG3Eg#}dOP%#BP1>>)HZ4o91QP=a+owl^Ic=1+M}8Ujk$-xmK;Kacv<5cF4zje&*rsO>flqP{yGhQF*eoDsDF<*Y-G7v`)i;6&_}#YPEk0-R#=YPPp>yOi7vAmHc<SBYsdwRkDCdJjk21ugun>>BXAf*F{9>@|i+Ot<y{XB<81dN#u$u#B3@zVyzv8e<V98?x1j4+fGDX_1=#xC=hve}|C6A!dFY|HQ*%POo{c+lvpVTGaq%L{Pg%9E5a|<8U-&)o&PHf>9Nax#lo$s(qjF-c@2zog{mw2`4UrVTVzK2ll%#PBsf0TAB=m<Qn%lx>m+9fdfy8z>t&R-%O3Z3XsXt~>T|MA<h0JyUP;IStFo~!^^mdX}dDqA7j7NnuNgII>NCvtrRY2SU2wi1LLX;JOw%pVETb_r(Dk#(j=*5Dr|POn|;xW22dz5mc{uqja4ra;|k3dj=P!Af}NX3SjRW9AYMi>Nk|f_MYn^~n2mi)rQ7Lt|SHeXsQ}=sfj6=c&id<^ylZi^VQ6+Gpz`sC|ZAV)sRlPZ~-kDR?_B!(Ejak$6SGBI%K*ynC-W5J%mvIUD5yUNvcwJ88dK3^q=Q@YHLFqs$|Yo=K*)mlutkX9|Cw$qYzEIfEk>ys?LBnY30l(OOkN-3p%;P+c*?Qn~oUIxUdBk=AuE5g!;sB^?<$o%RfNMqV->m)vO`>g4Tb(Jq0(bP1TdW&RQiJwTJebdv|uIVL1w&xLpWm`_L2M$tQCT_gOkh4#bMN2K-Zh_n{_T!WSk&pp|&EU?WuWC4@%LUGs*^`RmJtagP?T3^=)H*}}3@2zn~l=!y0Nn+E8B$MWz$ax3^Kls38Yemi4><aXloNfN!ps(*ZdTK%ii))A{MZ^ibDm{24=7E)%hYg9j3uyYh*%}c#GeA<)X;;9Tqzbr>BQJ(cw0BY-v1xh^AR0sZs|J6Glec#Qj!<BG^T39_U=3}-Ig0Bdh@*&IqVTg-1CrBuVk1COG^Mu~MKMYxQ+OpE07FcV%;<ZAAsWdPvcIsf+qVeXZlO~|**ry5-uBo%wnrcY8r=9LFUbDz<mmE9jt2IjiL=2giOIncJolUolid-|M33_85(9L#E`shUmyvxtdI<A>J!p+Dn%3CZQGViyD@mQpH@gVZ_+ytiY>o^CgY4`WYFoRuABbHZf!OfQ6U)(#bdL5-MpC=jVDl^qA%kV)OGWmc>jZ5Q2)P};4emW3KuEuf4bI!neE(e!JS+adv&vs$^H4vAU37L2$+M=&SxKR>hsNZ{JMc)fZ(r!XeX}d{an-s88COBq2aqOLkLSo!CX<boSbb9Aff@C%@azH1J*HiH%K&W;0CH0hr#Su^t=%2GbT`-~MuT82-ZhQ?m`u2MWWv?qQ;`M9TZ!02OzT7=z97||d=OELY1y{2U42loYlOSK(#E-V4{Erl%9ea&eIJzdt&!ywcS;7=Jg=4Fvy{4Bfkt*GyK~8Fo)D3mw(cQ?8ZhZ0*pZRdZv_;<6<<#pc5u)WH8g(U(fEm%SrxkkUMR_*5s>(dfXHVAM1Cd5U1Y@Ti>GcZ!=ddk9DG{{cKX)05(GSrNG)tyY(hpaL~-IGum=(GUesLKI3p%LiXi*qnJW)BJdP=+feir`B8*u`0ERB{m*^riBzx@CknT7FKxlgagw6sGCe1$xoBV^w3j`hD#cG!r<KT4>G!DitanNkY<O`@zd_euxjdCV@jEL}&ls)E$?D6&)(D$Fg84X}a<vBx*kM9}2*v|OeEz*aAaZkbc1R2oH6;krD#Eg2_TIbJT0CNIXKn}kGa_|bs@lZg%Pz7Y;sT$2g)wm9x{qgVn{0YKpG@iKM_(Njf0gn^!$&9}zv4dNAp!FVTy>o7zsV>2Aca`>@$%MRtP8OlVatd~d(S=zTL0uT^5;LNL^x*uZAk(yiB+snqvaq5{Bng0@f*Dz5lSY8ZQ?SHN!DOqDoTro^x(4bM>g=>41$J5?Cn90nYgzAAwb60fiv+tB)j%D|j-$v1nj|oKGPIIALrXr7ffHa%QVGBiRxiD0W*Rs$!6KL&yw)h{nW*a;Boh@<M0Q#cIqeEV!@e$pz#SNGHSwa&;t_3DkCYO?w4Q6&hg~3^&nB%8^&!cVU8LX(&QDDZe1Skv=3-Z%x!rAXAjWdL8wlHk_=QtaY-SYD0f{IJEuyTOBFYyG`cqtR@{!`HlC(3IPb6a=#vbKi(t^h5;q)D*f=n*;FO^{~i`L2)I$*f)0mE*5USSnKh+(g=hP}Ec@w^MaAFlX8{escXcr&deSTtPW<*I-#*4Q$wiy%N6c8Swg)S9hhNQk@3dwHqK(EB%+C>HfZTh#NWMZNG|^G1V(5qmli)%8$?zO9_>WGF%#kKOM!A;iq<!N4NHV>ZnDalz@u#|1ylkf3neu#CMWA~5QYk)8F+_f&PjzSpWXxB;ce=^8Dk>$I*d1y_Dv;@fs|8_5$KjH)d2Q3!qXgxMYEV8E+L046n~q7Tk4dk+(P-cXQ=G9Nti2W%Jk<8D%c^NUXfZtS_C?VKC1RNxL~Wy9gOvCtlVN%Nt&v?ck*Q0E=fE`kha&?RC=i)V@S%`ZOES3Y13_JB3_4p{Q}#eqwak7Y8Vyh9RXOmzqd72$zk22hWKzr;!3ANe70d<Y!vQHw(r3ApFXrUK?@1K9sm2=MSC7#m}V!=eMAIAF(l1~p6pd|OLbwUaWbxuv3A0_));-yMspg0^~+AG=)ysYfE<9G$#r3@};~Cx4e;+7n#dJa-E3oT_`KrcO)n0DK}GveW<$=yBY|j*cBMfMT=NeuNZppwmM<D=8kxTrAq-E$@vR__!YN1Tr132gQOud6ER+_JLmydGSC+?NZt`mIIj@!*dE5_MbKQYvd!NFTGhiVZ?)u2Oe6_0YIuFX{XTj4I8QsKhg)yP#iQvacnXaJIzq+G(!=VD2|tG%_zL61o0HTVlI2;rygq1YfO03tN!l5uCdUH%T9|Y2P->Gfz_R+xF<Z7byk}>z{TS{f~0lb2I@1$xyVySBhD1t$^=$mi*lSbO@R!&-Y<ECdwq{1(qVx&uOs6lOQu}`Z#5<$hK{_@E!nCy^`TfGZCtnIbTE2Z%PIq?j6lvV0&~o=e{*Ys488La3{Km#irz;KpogMU8JRYep%Duoece3i+})qf&AV)+MvFmMzA`mDL2hn(;{Z92vZ=5hq^HWwReUzm7AF{rkIFk-o5!vSWSJ=GN$Ubg?}2Ig;@f1$HSFF(R80?d+%4I0%{MG){5z~ORwHNtqIHE3yzon<xygc{&gy~2-r!{NHjQYPz~hO6^zk!)jfI}mL|`BUk0&acC57Riq69u3_@44k6Kd0!m!42tG0h?($eMeCELmR#YZljV2=l-PF(o|MxMr6aH|4qrI`CnaI9VB7imVJSZ7SNHiXWF>JU@<vQWO?SArFTTQ@tjRL~ZzqchXcxCYc<Sl)Ur_?Ggu{e-!Kz1N(?YGi4-w7iZEXFs$xC5FIuS!bDQRE-_wF>mq3_Idoi^j%BKJEK}QzW$N~s|3WUWoV2jrMWO-8g{Ck!T75fsCwH(*U}s0NCD$^@dayx9n%1{^w7x*ngV|ERB+t_!dG;je=Ht{@O*<uJyGB?Kg+{CK@wuIi&z-c5@Rj7>8utXmUKuod1sGuy4YujQyeYPDz(|e;<(}3c;n0w6y|MbC;V`OCT5=RNd2NxEEFn3$S`V6+EXg6eDmh!0zc}pfiRZ}?It9#F|5{UkBecz0SD<%L0e0<yhrUIgsFwMR;%b)=M`2=cgM|%GTbV{M;-W`tw&__ym1?(9oed8&6iZ~{oiws^T{|lm-WvqCkcdz!x2ncrUz$E25;BfRYz|Xl*-Uj0&D2=P(qI`&b2G6p*w}X>7+9gj%jf0BpO+hdUJk~2`8K$7GUYcA;iZtqB|UVPi0(4-Ss4}BA{{5V)O7fr7t~L?#OU;_iy)!_bcrds+y%Nu^A-`mZ(X6uM*QNmx#QkoAjH&)=`9Do!MX?3uo3eCzq>jgYmdZ<$Zx!U>>KZ)>U<@t&g{vrN@OO9A_d(fZp3B-Ehs5y<fWj|Ck0Io!OGjwh2DM2Z#G_IfltwmHZ0E6pJ9x-<Cql*)pxE-;7Ml!=p8BYlp<F+aDK4!9^t^MP&pPJfd^3YV1;KzU^j!m#>vy~5~8>S?=VCHnOF(rE9PTpGoQo{RjOU$n)%T3$H2=U122CJxcrfy`lP+7PuZLLG}_5Ocq4z1jQo`s;ZGolG})zUyL^pzG7X^+6)HBHuWcSwFmkw<KiRxY)UKF9lU-tV5YN>(71RPlI?8HS=(MnP4MGcpu8*gz%Bs!oQEhg=YO}LbsHccMQ8?Kikhy$7P(+8>mMQA8v2_h18-qlVjTJ>675g^m_=Z8pHw-#5chHf!V>>bzG;nNUX<!4#T1a4oYo+5*)(YpL?g{mP5M6Xwq9xyWJTx-FBJl)^geqayMdBf`K5wK?M$=9pvR$OfcIj2>8?zq$G-#5c18f)V5`xc2$^@`WEVjpu(D-T~y+Kp)Qan(si-}tjD{d*QxTWriTN*2F8LYTvZZgG!jnSf*Vu6*oG+zDK(RK?)MUOX8BR&FY4+x~4?14^4f)pF3PDIjXG(Bc*k6Se%9Im>^r`X;skoF+Clw<djb(c%IMgAs)A@C(`X0EFa`<Q|+;?n^p$h<nS^1BpZV`D(=uzgD483y?d13n$5kGdCBQ$gPnwuK1%79!at*FQqGi=<7xW0zC;T~7Cf(@fgkA$M{DCw5<#!jR#Iw&-rOMPT<|Q~Lne1%i5-c#)8fUKqAZgV?+UJfLP%9ZTOL4}H*a`k;p1BI^<t{EeJDYnKQ>Gl;o!<LAzeF=|2hw-j!q4SLYnZZ8y)TVyf@KaqpE%!Adk2doB#^>jY0XE-2pDcDOuOLKnVl(fZ@h0n-DNNM0X#Az6hf+MKf1=2gC@h13g4{V{JSj;pI%#`VqNa9Z-s6j2${<LaWpvs^~<_JR9H~7$jV3)wkpuh_5uuIH#>;RR((D<{6BY`2Z2@KJnz!32S20&j%9$-#xEyU%}_s$rD6ev~g90?@IOS^$VU*NPk<S;CLdfYvQPo&j{HTAHmi=NIqHqv?d1mSzgJ6E(##a2V<DRb)@;fd2|?Nw(LHk0PCg-s4y<i$qWBQ`30+EAnS{_)k*)Nr+tf;e-yT>vN=tTrmZU?TIESZt!2IWEW8ZQa9eb2w|F55kr_hMfE=F>J3g{8LeAS6ZRnHWk|9Y_GD7&VjpR-lFKqF$a@1Q<K$9$#b*eGuMwDb3L*B22!CKe~sN9)SaDk<-_W5+wvni7+9B3IZu5LkJe#Xkt4w%*!6G_#6UGd>k^_TYKNCp{u0}En8Slac6V8^!594+JkhTif0$!u#o{?DIy^Jo<Leo?uScB-90nDK*~pb=KRnoCFE=q(tq1aB;rEg@Mg&k{Fx<HTL$~7?W6c*g+Zc-HL;iO+^1oduXEKIqJVik^^mm_xu=AX;feACPX1&Atk?azqD<w_e)Zf@P_ge-G2nkSW@<*q;Ak(feI#%l<sAGk(QxYqOjI<syZVDnJO-xHPF)eLQd>_!SXM}!fKB45n6coEi(M7EbAYBxOUU1m0r^CpEoPP{_%>8h}Iy_-sH^I(+Z=h)={M^H?#HJoyT#EpImrhKjdu$!`;jR5hCS+jCtlibIpTooyZ6^|S9PuE*vbL!xwC$$SuA6RG=$+(sjnrhHye%l$GZbSaj!bG~0aJ&f`4F-f!UBVpNXo}d4?s*fCRepc#N+Ydt%Kh54_E@bu0bTQ(DjM%!ve8^A&OYso7>AX?!r4>r(yqTJm9iRC7IKwre!Jk<VT0`+AH9Z(fah50t~$u5x!%g`Ht1DAY#edPDTr%5OsM;-&j^^HuzcLFql|EGbQmX(#kWb8?Br}#C9+bFZeP~gD3O!0TO#|kQnWWb3nwZx(usbM7rWC&*mr$n*)@<rbtU|HGU*)ze#)Ayt1dw6QzBFbgmUm05|O#QU4a`D@4pV#;!dt^D+q2z9R}mvC<>S97aoXT|}bdo1xH4JS5=qEc}po-9^}>BOe^(v?1IyIL#!XH}twleCQPZ8fnN~?Ceoc-Z*AxI0!M3<DO;ft*XN0?QLVXw|#GWJJ{{5yxmM>U#*FQ8bAg{Q{WOib!mI!6A+>>9>T0g=A)7M*!UrgCg3X1tHc^;+hScLT1x_bjYklCmntqDQ?(|uL2yx_RJ{E&%bY7LbFS_&=Nc=r8mz`@+6A!E4Ax}<1Ub``fYIX$4QE3zaB#R}145$)e~Htka1bZTN}MPk*f~-R*I6;#*qdBTR!b-Q{S!IUDxMRhk*|W_?!X~J=0imiPu@<d#tj(0K&UY65?>P^Pty#oD^T}owZHtyj}ROrK0px%yL&p|x~cpn?z>KJfva0QH!2O0YcykQ@T9e1mk`*w=Eu%89y`~u4#B#F&>zrerr<d<g^e>40nXl$qc!cw1YnVcMNw!nvdB^{$fgJJZVtOZpMxQOPr1>SNj@)Z_{=ocrO{ZIzKL}iHhjQ@%0tWoS@RY>xeMvbMvA5)#i@3MF7;g3NDrBQlvb#q`6L+m$`N{BJW?D$@^jw(?sfrm)W+mR^CoeFW-I$ZqFwS}xz@}>3sMb{5(f{l0Js-KWNh_dj5JbjkxDY!F<Rp?&euH<{7NG%@{tIOr{Kz+eI?cY=Mlc=x)M8ZqT+V|LAP3r$C2bF(`SK5<kD7UqJ0)Dc`5L&s$`cCdEJk&&F2l<d`j-zQ^jp6zy*28H&J=ox`>6&C7keZ2SPKnKc3kBcwyV)^(NkdXgt69AjlX!8I{>CI^VVc$>30f60@r}{?sz<64>FMj6FW2=Yk<8yqqcDs81hYYBeNPpS<KKdK}x?wym4*0nF_V82^b}%#Lo{`IeR3urD4C4=*Und!#46@!##n|Kg{a^td33B&F`{<42__pK0+<te#BDhU0E8|EkVk;&26Yrr^lmcm!I$o<PgagRHtblgl(VELOY3xVzRQfYp0r&;Wr5AjeEg<Tl~`&WTrz6Wtc<#^BHLgH;8`$jX9c<!nXO2w3y9`(n<fJ#&WqSePF@$y41eHq|&TGDDw9LA}FaV=T<0Cq%!H`<gT_YVI=G!LFt<vK{ouc5cEyf?aQD&z>6^CHL{y|Gd<^YP64_(~f{?R~QoMbrA&P#5@b>g>azmDpRq8Tt7%D-5oiM!=J<GQ-I6DebE1n8LYD}NFDG>XsfH7J<^_JWM1guccX{j!!i2?A`48~H5SH@=`pb!`4D-PNZ`RR!2^bgJ}^x5;V!n;Zq|2ehf%o{1^#eE)X&36Mp<1*$rI>Tc*WI$iI#Uy3QC*|RJKApav*q3Arf8>qk5h%z#a_5n0xeD1Jj%i#`N@^9)Hm{Km8~=kESdLo<zHdC)$C7fsF3X*8E!{pdx#0(Vg$_caJT)e{m+uE0-wCB`6Bw@sf$F?<M$Mm~oG_lj%)H-DBr;2RmojSQ<iTk$9nn1GyOa9f!d*M7GHeP4ulZ0XFp#&BFm*<5CviX`>-4o!<ByCy{7)us0e72AC2lT}9+|6^RG+H?@6wD_ukceOK!Wz3UH6V1`|RG6(~YZ;8AWF{+JMnwZ0PHIs-@%%0fwW6>y?(i5OBaejDTX{^O?aS~(T8<f#OfQ*T5Pl_1-?9-t;UU|GgHt)$-0rwp4B6<=NTv6YD!ndh$cC!ZsTzJF)Z^jP}o2~rfdpe4Q^apjj0H;7mA2RnOw=r(=tFyf_C__(VrK1x^nj8Y|>pMD8HIt{%EuiKAG<Ti`7d$jLz_&s8Wi(4laadAfrMFc{9u_z7Ndu__i(P?Fgr&bm*v%9dBMnSYa_9ico?2V(@wwz%(WAjidtE7IS_@dBQ4~PXou0fYdU`z3fi?nrhQh@zF&-D2ah3_yusD#+00i3Pe%-_xZ4G-Nn{%TLCxbV`@aPaZJ1p_`9+-?$d0}I>ON=E6DK+J-TJb0V_eXaI@Ap|lA)_(biZ<nma06=qtL_0<4PLGsZUpXKu8qWStndW(wiU*R#v`IVPAn5WdSctR`%34d#9)sS7lTA)u+$w?AD8wju#%a}LDYf0vg;A)>5`9(2n*X&sv(Sxo;glW$Or!eRD>|<@I|1_5kAfUn9b=2`ULWB!(JaXM*7Dn(vPt#@Yjydpe3NvItz~yWFB?=g-_{?{=|X2XyIoT^uEjvz9bJ$?+$MIxD7~Nd3P#6^9U_?kO)|5&Bt&6r6*6wa8W<faj)hIe$OD(nTHq;2WENl63*yRnI?8Paj9ka`FmDo@y$UY?(`{SdZ@r6akqHn*`C!o$gZ*K@DWZbc}sJOzV<YZLh_&<@~%+g=kHl*K^41cg+B!{skrK}V$jh~3iRDA{9OT8D#f!#c_XDps>iX>J$#_+4?hx!Rrlq;zWjgK9(|b')))

_TASK_ACTIONS=json.loads(zlib.decompress(base64.b85decode('c-q}vU2j}ha{MoR=7Tvy%68tk@~kbaY#NfB!NwpK3uJ=;!RBF;w_yK!v=V3L&h6@|>ON;kc>x0^hT`0N&pjXA)m7EM{@>Mq{P}Nx{mb93{^i%JpYPwlzk0mB`p-ZA_rL$o#}7XK_}4%G?Z5u=zaM}8_3C%O{P9osKfU?!{_WNE)$51-)%DHe_2-X&e)sU*FRwp*{Cxkz?*8Nd?;aojetq`UZ(jf5m!B7Zm|W!j?(N&t*L=Fb4{zS>uEY=I-i{x?|6#ZLcn90{t^MwoH*dfD)5mB3@XM!fJKoviuAlz))0grOPZy8>jz8*p#NOV&-k|~e_3EdGcOQQE^xWvD{qFsTt4BGk@V(un@9pUyY|n1w^QEpAKb&r3HLR2F=l8qacjxbD{rcd|90t>T7542sU1~XH)>pblxA?Tue!Y5q9|z|jmwx|`=e)l9argG&r>pDD$N+u5#5KOP)f-&ih<w!d55JsEx$FF8=m(UKv7U)H_zj=d-_!5NBR!2wGFCr*INsmtQlDO4X{Z*f^Zvu`9lu0*u-4zSxbV|B;yX~+dm8C*y~8)a2aJz(oE?W>eg0l=4W8dhJXcmn)^bLZk$(D}dh#26IW|$sBW+yo^qq0@rQ_SXTJqKK6Evv)0EX|mjt@(}I<C6YpP#m>I8o7PWh?A(lb0MKu(}pIEf|}p-_kEVd;_}i)3=A8$R-EAk$jQ$m9HP(zTLh4@TcGJ-hFuU_RYVY55xI%Hlo7Qf2-?!_wM26t3pK8IZ2MAdpuHBpTOO3@#G{7*{CRObAG6yVMY6gi~-`Qe0sg{Ipx<KMi_)oVIbmo!f9{EN$A=r!bk>hcYnAY@cWssHV*l5B<MXHe^0lCIB$;u!|~gXKNx#3U%}^_C4SHOFGAGiY;wmy8!VCK?Zhuf?`^Y+O0s~A-N-soORgTTaszg<WV9C7J-)s8VvP}v$Mx~ALG*8q;td|ffvhx3kK<B7YvTG>c39A0K4zMYJnHnv$9I$k(d2vMtIELv>r8WET@vg!ZWskOrv;pcYknBJn)^5+Ym5VmG<CegM&JTLSsw6BipiSbT@2h>@fui+g=N`@;8cv5Y<`7x%kZ_4g?7Au@F3u$48yr}V2W;Ky+t$;D;3t|lgStc2b61smDf1?cT!3+5?P!l4vSw6#0~@}n_ln-A%WI|!yx~38tl?BAh7!Kc5hd~&HE4U?)Sgjy?ggZ3qD?>jMos*;<>+n`G_<eBM`cq{&4^9U)kKS@8I-BZhVyvOYa5_NBQC(B?-$aV89<a3k8fi_|D}J!w)-wOMDve0~!%4nPev!x!~#HkB@hW%ba#R^n_K=l8oQshtq!A!$pltu+3@C6_zs&zMe_|I%C#Vt_N~egrpjQI;nzQA_UgRHi-vSRK+6IERG|UvKSqwr+B4Cy_t26vKZRBAsW52fx+*g7-`EW>-5Jecx>fGPhYA-*YvHQZtFNx*m+rioY%|pR)n!IQZN9j<=hKP!ycd|xFaxbaU^Oe8`Znmo*|FK>M-35qz7p2dhx%G{txHP>1EK9u8`Q5HY{=&vltB@l4AjI>rTdFHb1Jlc*J%B1^w}z6u*^fxFB(GE<({hCu6R}x|$o)dx+H!y+uFe`)hAHnNd4;xM)cWe>s?4L)RlAGY_o`0rl-@oxhCxYzxtI2{xwj9X|R?vzZ>_ZUN4ZVnKK*Cy@<zT8~gHF+;4_{&o<}CA@~I1Cdw021Wu@ehMVUI1=Fd3U`}?drm+Y@`c{mM{JYbeuD1m*c(m2k+lOToc`C*>QZOY#V<VGpT!99Pg8WVe3{=@n3YcSFz5Cz9@-3r60L`|QMgvs*(_-egckRSK%rTdR%dETIV!~)1=yl<K^8z|>BSV}jtC{vu%!5CcBHb1853{~#Pl-ACb7)%2SAANC#N0WEK?T7?i+r<2<s4dp-<V6th@ZI={{@Ro2|Oax)@S_*a}HkzW(^+vcdy^!|d$v%frrtGax}uW3XT7GE);9;gpCb327KvntX*z1TVD<poQ=odxVQ$fWlSI750q+vx7@krfPW6mti@&5$M+zY33BEK!Ot&PdX&ZQoWeTjm*n7<SCIS3JN*bSQLp$KMwb6|M2kff3Fnr@f%E{kGX*ah``_0Aj^2JMU6mm7bxX@8gzc9hv9mf>~HUX`tC|c=ErLUEpvxLh$f&0X0t~yZ3hZo2{9#tmIGO^<v0;6=MmH<uf9Y^6x&CCmH~ne+@Hi73x7iFDo(opx}Cu3c7cw+KeCAxfg#fc^8+aR<qA2?k4OOqkC5^_)0wUwL!`%jpAA&gJ!x>)yu9PSHzhZULkQ<KFiK!MeBu((9eOI@2TKgiD|57csxnvp-)P=V9MkwoJnGmjH+LKJBshP-tyAtN>l`d+Q0D-Xf5MIw-$h7!`SuBJo-AAxUzC<ZEEvZpi0fCag49|dskPXq5YFwA;i4WO+1_8C13;)8FLI3E$jUSp<b)%W$X?=#GPX74cx2opN^Qf1<G`&2@yXqt*`Y8qB<K7fRvXl1$a08)2Xe=WApXFK;PIGk(^fLN<P@YpzKvX;nCA@z(lA_w@YWbz8Pp)^NgV?fS_V)`l31ly+v@9tR64F{^zS{&q?rLvi{N|Xy>R_dr$sBDO4e3r4RXdqfc?)xOCY~E00_6$%qmSyZj;;(ZkFassLyd0O)7-ScyaZ|G9<s-N5A;W798Xf03zEOOu0l669_i~TnQ$NLE}nOK|QW4<*uw+mIy7!{!BLLLWC3<iyI|KN@Mvj`nR0;Y*iZDrjAnHc2bZNT#Irj5DKuY^qS^mm&sS0Y!twmIc~6>k-MzpWCm*Cj|huvUaCT1#khZ*rixEjqb@+;seP$j&N%Il86(sl?}y~YV0IA@t5wbp-x7Dfv$PJ3(mI=x+f!@g7_>lX&tTOyn9$rV5G+rWkT>2LSa#^Ls7yykrNIB~+CJ8QA~yjl;4hbcA6CYXZ{GglQ(ch9e9(waX6JSq{`BO>n^Ek7o9$x(<VaEm_@Q5BZ6xyc(|~O*>Hv<r!kOy^dZ-ym{Y?cWIo>Rw*-y&cZ4`vzX<)a{>!5Q*Ey>*;Ndpj^@jQmXa<b~m71Cs!j+JtMb-3GwaePyfkHNwhyC~Aru*pp|-Wxcums<k0bn))eg=U=K*(*3{7!;i8WN75D5}&Gp5)QaYP*6;n$$8<)jEpQ5xUF$pE+U0#(Z4~1%^Z81Yw2{41o;6Ib7=K!s;ft_=#r0@H!0_Ik>b!t-E>bCS<qrAp|7Q|p;idhz;MMmbLk8v@G9B5P;>-x*v@EGU2(vw0TCWBd}}IWfK~#)${?_d^L=?!ZTOiHE{Ih&eS>pQ5acyT8%Y2dr?Mq{5gE0|d0)QKuV)kA*Yv3#>mBd{3z;es%7?$8T2uXU&vMMHYmurc8#lT&$@^(#=rhszR+J7;w+<F*Zl{{Ym4tJBiyZK2gR)}|7za8g);Q(|?H2AyZ>!Y}>+Qy;aWmIuhX3=BCI;drDZf(p?x-4MYS{obfGlHiNs!`DokNFu0H*W|vUCIyVpsvrdvJ7BX7{+(0WF9;Ra3Z>D(l1mp|wa_71eS%lJZVZyF!5~12%~`OXg85VQ!KU7>3wDe8o*#Vi0YR9lubKK6$aLzs&V&WoJgeu*S=LVBVm9FyIJUp~KeuIsf>>!;kkL9;}A|iBw^gfXz|i3ezalq5mYCS~NgB{PU+_vqXK}u872>1kD|=BrG{h14A^YkY99wGb$yrE>{s_VrNvTX%7gF*;3y^&B9zy+{L`h4SVkj5YVQtZSv$85jV2hE)J|4oYGR0MRt?4Fev))l3Xxre95X0Y{Utt3QQiX$8HWdZFoT;L1I9RA9pu^yqd&e@#ejWI)hnpc@G4@QaEE>Y-yHvXTw2vxDLDgZBY=>>rl!$7%{9WsSXN1MY0Mhk8ktWSIYYUTpu#@>SJEQ)k^uiBP!f3muB+n<A{$MYp7+E#Bepwmz78{mt7P$vvq}xq0JO3rIa3wk&9wfxE#GW$3ay^Ip7zKKS;WvrZNk5DgT+xow>rSy!>}W?oM|Kz&tcPh%dmQX=#H>zrC{pL3`E%`2ae&Kp4KfRamKCzxU^Je<14!aK_OCo!;@zcPFTHbbguwugoWAN1j@LCj%Un!}ExSWjmBkx_Z>^Tlec9V8?-vhHykKHUS61nkqQsb%R_3Ei3Wjk3U$vC6r{r`A{nT5KmZEKL`aJNDraU1-f1K(pc~^2-GGkJnF6G#59ZuA#P;vK|#G)#!4uA1oRa22yt^ZJCu%qSr#V22rOW|Ak7A4hwmu^ri(>9y`h3J4GtTT_U4c<FSapKuIQG5m{tchWH6v3OMAxwl8O7eHT$fP!$guO-oyHs&z*(~OfKD*3qaLOYA~}Sv3u5d79~lRR&IFnbqQd*y_9wd=@jCfRzA$JqputOq6=UNN~`@Rbtugix@3ra@6@j;9qX&)X)EQ!wD4L<CmHQb!`hOoT?(xn=5_$tm|}JXDb_%q2uxN&`{nM+C>hL{XgzDbY12&X>0k<Y3^Kj?CpBOQ^`Bjxp~w6#zJ39_F=uKRLGUiNT{OgpnxVWDhl8os8(B>pCoO@1zJGXlzZ(Jrc=NQwqb;xFk{Sev*$tl<0t^O}OA%4_qQs4ifL}!{av!ntO$(GWFm*NpEG8qg@;IkFvC=Ub00K>?DY%t@s98wBYc=FPzkuo%J_8r8A5N@kBYR;4(@W+4XFV^`;ya(Qp^4FQ3qd;s4=kuuXc&-UbwlXcz^p%)qhJVw>sv(6bdEY>P{t~NK4y$Qz0&bLBzml!6C$l%(}b}H$BLmPO^<zE47~*ThD~`>s|Uv*M%b5|>GG&1N^Z!*Uf%q?*|Yp!+djtI|4Z`O3TOgm425omXdlewT>D)U?D4yy;F$Q+N{g@vLvV}<<SowwJH^Gtj92c`53#yD`GkTl=@>MGi)JX3E2<V9Mq(i_5Z{Uma8Lbh%nykw=o>wfWtrA(Qdop$nMB)!SxvBLRBeDVKyc{Q7y*Svvby4IS|_XY#rpXo5lzD6XZd0<$t?Hurnc)%990aT?=0g}>BR!BeY}#1jW)11@e8=l@R}Rarc=2n!+LS}?)fR^@mB|y7ZVKMsBhp60_%C=9$$qS-wEOxWFfB%xW|hSN-%1_FrgVhJ?KcSe`anN=R~$T_399ni|!O7D~8&e5eg69btn~~3+2?gs)!+8w;kdp1p}GmB+*<paTpn%v7J@w`3#yl6ScBf4!J`n1oLJ97}4Bkwe`l(8FJS3rg8b%m*5!%OS<!CUpj>Z;cR-EK7&Bbf{zfQWLNjg4VV0UZ>p?2+fXu)o9ZX&*rf>AjQSuyj?Nzji|XMq%%+F-A=xb6;%8)G<7kNK_GalL>3c}M@W_+g#47x)xp}aqTtM$Q-L2#nSnW3@mgHB@2k7-Rn71_yum<<J5S9Pvgi%9&$m=Qw765Utvi(=l0hAyxgg{3nVXi$#{q|wydkV5bo0h;VFoaL5QJRsy5?eKcgOw;0VbH$L>FG}FXQ`2L)N?r=Qg0+2r}bfSJ(|?g_I$#Qj%g5z<uxDKanWSUK2(CI#MfY8tuT~K>F}y?zf1+j*GcVFi3*5<!6*}+LZLWGt1SeOkx`2Pn9|Zf{^@lr8DnQ;&QoC7<T-TL6~;{>Yd|>$Lx}Z~NJ*+7F6F2Na%Z{(D+`Y`;_!JMF0~U0ILWTz3mS}6ken(!X)(I84CtUK+>7{?K)D9w{<e)a+zK`^qukm-Kn0~LVrj}^#7e*OHL@InyFoAq?1?O_6KAXLK;fd3355`hz)hP(Z8Ew<tVI3v$qSYUxhYsMU$n3^+t;SIsXZa2Ygb0ypU13U!=5nVvuROgfi-ZubfCz6MSFhRiOgvhkQ#j<5+JP!xe8QkpuJUd_c#jNWufOw@$m-XJ4O2FVReTI{!-|jpx)82R1$@pvE5Emj+W3p(H2=`#PkFst<RGP{aI9{$qRqwlcP;fGz-|+6A2IVD)wcXFj!cDx?^dSjbA9|FhZ;=#D`i>>jwDFN&-4STb;pEFx!u>PHLID&JrL)5sqlEH$~-PQ49I4fwzlkd|Ab_L?vYHKoi^u<cNegh2kT$158>Q65=wr?G??*`R?|@%fbi3sGJlW2WGR938W%=7P0Psb`!%wxbV$Dk{*_mN$G^U8SJ}Vpks_+%{d2OskFtZ1Ra2=HO_=5^c@3Ll*3^rs{b?~xXZlED(XY-6HyNs_l84bpCjUL{UV78umEix-6cc;7?kLVGnZ8>YMStowy9it+=Gh8N!b+&1)F!~bCM2m;|5^~3{O$Tgl3mhB(i$SSZ`(*{_55Z7?m;?FmQr|UJhIkf(;i<gw*Wa-0FY%vM3$zfSFFe6@2qbv}z<lR^0SMg`|zkCC0*=W<$+Ihq`F~Bob)uohxkLqWQ21ZfYg+Y9yYXi#F$!KrJ{SlhLU|nhi-Q?|Tv7ByOdq?9C1CTW+k;cq-D{ZwWWqGC>l$FyZOF*+tPPc-(yTSkaM+3-XFhr}3tWnksM47IITeD5mC62u<6WWTx4br?DEZ5Nphq#vJQ2f}wP`Pq)qEOH_e59}r*_(l0WucEx9sG$^-CfMW!aJnSr{(F)MBNz|o0hdx`WloBVnNiH)FKZe6JCGTKzg8c>;COJgy6VsD~szN$P4IUhR6SYaZfHf8ARA9|@FpEmdv~-fqG`1oebxqt}A!%jt%N+OuPIlKO0x!2S4e6WjpMh;l(`mL$4z~xB9>r2);P0H5V@(>|HhO)Brt3Z{@O2;U^B_aC#_TJ~d<7G7`#9Q1x*AY@tk4s1S*YM5*HAHN_Rafg<X9fB0x=GVqccd8DC#UX^3xDp{4CtI&6mh+tN0l8C~c$ub8S)^@R}3!wjLVPm;7!!Eg@PY1Yb|9LK!I%p?f5QmWI6MMs<CrgHF+PZj|%ZO8fIYpW+Gk0%zG=gaaoW#piV{D}3B*&JfcnAmL+ktG;js>0hIu%)X$mZmbY8zdZ518#>Hb47ipYT?0hCA{jRGJQSb7CXaepvpPDjdV0snvKTml_vWL*rfWjJWiyWBJe^O)PmdH+3AE+CVW(m-q)#-Q_X>O~8UN7!5vJ`@eE8{tHEOKD17d~%U(}W}&QNd%Ac{c6Dzn+R;tkAT)JoGj@AOI_lwq^1AQT>C(Pj_F1>}lJUud7fPjb(aA98(5Ca-iaoNk{=tBVN3a{GWR|J?z8HNeSP1UHZ7b+|Dah&u;Zl`ke1Q)}v($h8|0^O+1EYxn*4@Jya*sE1V=34&=b=nVP$XtRmTQQ?b50gE3tdr+LXYA=ln+871zyfK0WZVOo81uX0U&cGD@JxBXzQL)OL45(WRf!`EV&oQtA$X~l%#B2mFGs#oFMb2qz)kE8m#^vO$u3XZUbIe>=e&Y_B3vmnY#>${x<GZ|Dm;sZBnL2ZQG}wa9LZH;2=STV=Vh~|rvv|_o(`~?S3`;P%!nBndRQCw`n~}paA_l%40~M!=tWO$<;&lYpKIX}xtuum<)c?U0$7q9ximjOfEPV5NgSiy{$y5`5mPZrKCDY=T6k8MMe(niuBK1_?x3{qC(T=ToB2sI0<B-H^eIdPetA&<FrdJ-`K>DOnN=(WZpiBQcAW&SteA$Lc=*6hJP^C!#L76kp1PYWQuL=|H9Z-|*VJRU>fPoom=J>&B46N1y%5390EGHG+2sU4~ko2xEB)tf}HA5M?r>H`qYLTl%o6S=%D*lvb2;SamxyuAO=vK%<o9^gfYSfjNPzE8K(}tCzNJ5#d*KI{RUocK<C74aB4hg6YzXta~n?MbtC}NovxE~SV4NET^)J83%L%7Bq?mSBnwnCPsmKPylk!}^s=5Nxwi#Ttu|J97jH0Z6|Xih3x{NYk}ak13w>%i+MG<CtNB+b7rVrFO5Od#tMf+5DVnohRS^eu+j<Xktkp|BRxGnR~N$fyW4@tpwlV>mT+#HdXxH?iu42x<;gzE9-F!j95M2`O;Zq^S{oTvA!lEVcOjy~YL#caFB%Ez%k@qLR}sIZues0*Iz+=6juoG_9&M;9#6m!t8W-%CZKkE(UB<JC6S_kjawSDMJMV-#3&Ml*vUIV!G49)@80SZydA#sX>C=tF})p0YC7g5esQ)EB^%3Rp4R!%whmzw$9Gy-8hZS?67+K1rpeDHWfqhZj-&XNL;&^GWGVQ*=PpwEPL9v_7v4{JvVaXj}UyOo{gF2^FWHqO`DUZq57KCv=*Ke?2qhj3p16bG*Yg>g0+w9hEqgGD$E=?3&L&h_q>!d?$-)ZS;jr<tN;SDQsxhZ06725nD=8X_W;T%<I0u>ZgeqpvoVod81XdK)OzP?)6)zkid^>q?3=*)mH}`<Rn3@Tsr6OF2zQcTTG{-`Rtc7+lP4+Ufp(w081>z5Qh@eMnKN3UMN4n&GvLJr1eS_}pZUiAgCs0TmEm%JGZN`2gi%WC^4)2FAmOtF-k9(ob;YP{<drdA9C>1?_L8!H$34~Zeav|Z#ZdEFyj{R)t=7<ka;{u}56nn&DV4RFW`j<?>}iNX_aF*;eKQO8(p_C`BY|3*hf2`EXf*`yeDx(_TZQ(csV{=cIxgQ!^p(ZJ;?$lQ9Ykm9zy!o)7nrpJ)JrQZU7xhfOnjOn8VLD|z#5FnDk8D2?@V2S%s5kwbM)I$QUVy5&oD3%c{h#;oROxv{azHY07lwaHME@=vPUmC%ed^a3oaUufCp1dFhic(8_*`!d5!oYj>@tzwuapo;zPfV<GZMi;xEf3j8!kRkE8wW;gcnt4-X$+!qea4A}%BKBn_u=PuN*nGS;3?_J5<>ZWp|o*F&<V%w#=T#Y<vg*?z>no7NQyPIEk?^jIlEQi3iau|~2klC(t<QDPg;DY8obOj+v#ga2L7hu-wpG?k_kHqc@-V;o!<HPGa$|0rtGF)v-eEy+0FGueF<HY|W(gq>ss7Zgnz?7&{r%|^k$ppJEVDIaYu0a%qXl<LhmJd3}m;`K`al4YZ96S@?omse8Ws=l|f@%inSpp%3OYEC!vI=aKhhzdxP=e5<et3F97CLt>H;s{+y5XopD1%|e|V}wTVjjxm!GV5^}^%a7_3aPNp%2K)Er~r~59`Hm(DZip(+1<jxuI0ZqR&gt6z=q{%+(OG@252W=?bBacE{sfAH(QhPmHJAMRWe`4NQ)vu+ZC5YO^(1Bcpz*w`o80U&kHLrRL6;wR}2K`4h>0*NosFB9i7f}1OB-f@^zFSg5PyAMUc)HU+A8YJ`!Bb_Jgt$$xG2!h&heo*f1+PLJV$h5d{H@*${zLfJ&!@Zyqm!EY`op&F~i0Z%3`eX18ZJfLnB;rL7qAFtIa8X_*i9GC>+uD&jY)-0FB_us8Y(82YO=F6s5gp)m43kL`-yb+uZrH*E<pob~@CnG(p>Of<|z_4wvQVYy*t2`|%7sO*)ElzmmQ9$V}&2e`zgvVl{q(RUzkF1h$9?Sm6lVhUMXdU$<7tgubHai__DysXqwG~x7vuqy7fF>H9IsT?;c1}EI!3tLCZmU{^SBz7PnA&c?SQ>*-*1wSH>xjhcO;7i3+6E$Gz+AEksn<9PLD6*@9bbYSDvw@JDI$HXRX_)rIh+WL*hMINfy%c-8N56L?)8!N;Mnf84E_#%+p0|FB`+0YjPjN%45U6CU1U>bQwzLz3U^sh&nYY(HBsUkzqV%cCFh&xSbzv~~=nPHIpJ$_saXy8+^1Zt1EM7*zub--4)lui*-ZQ2gCr6idg}sk+OSYR0)$lbg<CT=h+?Z4`?dhVnNv+4zvn7U!1x#z_+Ss_;K@cOFiY?l`L(%$YXpf2TFa?Y7qX?-oBiV_jqcsc^o;srF3Kw}c;e?UE1VQq_o3BD=WUXF~*poJ^8|XVi)RUQy|Ba2ZfoIPiL7q21-@kufkyYXY&neoyN}znl%>ADWd-M5LBkeLTCd_;mudz)5f#a*C*X1(ac&oR;Z>7^^QtPa_i48Wk1o!|Up>xv6OA9g!;?m2whz**DF&w7>ZS2$X!W`m5cjRcwY|wMa0_bMW0IQ^gLGVjR2<*49EWoUAY|8z^TW@m)MU&<ovXiJ<)ZG~`oXoT(eW^t~M_R_8hUWT(4(%K=G5eBr&IMBxnjlIXq?4_33@?<a7$x0sviuty!-)Q8g|toh(FdwCCXg#w<)+ePR}u%=-ow1;_Mc^i>pgb@vK2s|Y$;PBXhBk(ub&B}hO);{6m<(LfguI33oikl4G+89^H#D2@j2=$-<{IN3|Fpj<91hArE~^+Vv%5TBqnV$_Hza>9nPptzjVkAfmd(;04a%S3U*$bmv(rh-y~ARl#UyVv4y;~4}Y^nL$=fX=~Xhoyy+8budRVPKR;;;7+czgHiEaMC3tq}ohe|wfOI%@t^h_pCuju$)ecI9LijFVs`Hgk-SQPmI16Wdh`7Sge(e(LnshBn4y~1~BG$$<d|CSFHi|4PvZ~B%Gg24s8m7}=iH2r1)nPx;WSln;6<MIX2jyu7b6uxw_J?ALgn*muO{8Tg4+Cw{9<~8B#e{YiOUHB`aRjKg_pD_-ag0*8Nx63%{j>Vf3!(&nT~*-hb`UrNla{?FftaYgjKheIHt*Y#H;$+J!6LlmxhN1l+-s8*?gW~qZLO{i@okP5)nY=*WuTyx*LKbX3NJ+>gZnj_{Ib1+`X+-fmMsj|M9F5vt<CI_%_7Stednmr{-4=OcY|_<-~odv$sil>TB8b5UMFD4BwdZvlk{oz$nKt=bqcdu$z-O=ykYT%K0P>lGj~9YIHbVja3$4Zy3|HnV|skXe*%KnHihacK3jz1<s>U}IbOCoS5kx=B6*zymo%XM_Hm>kUi^g0ioXP2S6W~#Q1B}4A%__jR;sQ_*_3ItDx=J92x%5pOX=|>{+7$f0U2-f`LJ@p-V)f?d0I}ZM^UlQKbnyIM9~=F44G(KWZFd0%`>!nbar^wE41eRCYsY72I_(;NZPz=mo;gpW>CWBrPoGH`{WI(;|=fT3+w0@^GO^R{58y6KQ{eN5awdkK^c-Hh^AgNf>x9yF7Y&gjejxIGvUY9fN2Wbvp_&<bvyc<skBVhIsv6%WIaer;GwEhqr0K<SM@Y=M*Yw>`6Eg`(Qytw!0`pC2(W;a*9wHDme*?RVnef{U^C!e2G)PFF|k8RRc7-2U_^@eZOQbi)EYFh2n)!P+sV=8irE6iZQ0Kj?~~4pE6_AN{dTI*yt%kGar-4gSK0*ROTek>wqW}P@1sg8JLp`W$^OgOP&!^kFM@7S6R@2jJliMz1x6c2+D>13gHHbN5PCnWQn6+2l~Bq0uH21<Vmf#gymf|i-U3rpp{~eug#t{VEZCGH`mOqW_M}4s!mGGoku}qZ<+x0;_=9U1O{JsFB0QBl+F>=AGinyXf&p(a0L4Ca?4qoBiI|GT`^rnx(=r@5!OqL`CSsu}CivSRE^<M^Bh$`!R@#EVMTtkA)Alg(#}f_TKb$r1HWt&U&ej#wNu4tWAsh&hal94Ro~qvui>%%&GRyegHP1RVdEA}?Zjh6qtUV3(#jCnYc`UR>GYYQ+Y~X9#cFatRcnrrJb90<Ys;5LPMI!cE9q_tc)znMHppf*+x7;Ii3mn`;d&wed#Ccg7@#LnR%%;oX7JBIV7thKX&b54?B_7cO63fj*i6vNuEpM)FtH5CvS32K@-!372L11`{-@-x|6Jjg!vvdY<&R(j4EzO3Javq_GEZM-P$t9;OB2+Spq-1$ojxnXI9yX2z_cca1ivI7|)uY>-MyRZE?5lLw+F-;9K^JdcYA1{X!DG&tNv}o7NH)4kzce!?jue-Hu8*b~i;3-S`v98d$4sr)5|%uiH=}Yb2s^nB-Gx_?_Y-s5Hhx+KH(hrj-tj(Lo~rX96$Y}V(>dKl^p4!6<o_(FPtaLwJ6CSd((4`EM%`aP?=qAgMpQXe-@+|y3Oc<F0EndaNV}$q_9%O;LG~b#7<S8fA%(;z@a-_##~*AlZq;&1k7J>eQDokreZ`>-9gd+pM4&ND%$4Ihr}}~?(p<v^B)S<R{<=`UV{&HfgBI#}=g^|=62NEE?mp@zsNi4iQw9}$^gwDVgb*)-^#n#wJ6AO_YhGNKYN6$brOpXX+x(yvfNrEP1?*}Ha??n+Cp(zSZgK)Tkv>yCI0aUwj!l_=N7bUyWDAc2K296uy76uig}}>!2YD)LE%>Sx{DDM}4`ZgiCBo8@>)WDG#4ij-QGdbgpqmA#mwt+Kyd2l#x+hix(ppb<nBh(YUOClGy^{%HS_dTk!X})&Jol~56sdrw^+1J23Z+?3AW+z%HK<3|M`dnv`%;{HsG>e~|8NXu0wYUIZHDVrtZiijJk#2<;TG1<*)8x!MOD=Kgd5Ei;Q8ZKK$kAF1zXW`WiY>GJ!|N#<GqI06^2nAt~H|ft1*`KKHgcl8!Jcw;9i_KU{V!2WmF=o60C!E8{zA|a}B#p9nRTA-<B%~5;(U!p7zDVX$dwkFo&~n7%nS^H(_zP-d9#*$Fsek8J~aa%G1KpXOHhWzV+gS9v?!0rA;SRj;F!-&~~2YfaHX4s^~$TCvwZr;!W4ADcmgEyKVMv=skj%!d8r`Sbwj7*(4(fr^ReT(*I%#$fAG|hEh`!N;75Jo0Z8uP5V5rlV+<Pe^N<X+L3v+_p>ui4Jh>rs>Tw^CBl1^HGgsyH`DIAU3A*4bJ0>x<vwXFZ@htY_p99y%PnXlW)WICDBU*(F2HU%ma=)IC+4zkZxVt(8N<>Wq;V>k9BaNrt)p`-<nHnZwPz;!$sYQC4#DYl<hHY4ne&@LM;kZLiw}mPJBG{*K353<d%BOtYlsUw!U*HHJ2$!(yv<#{j92M+IlI1dpM-Ik>8<uYG7~ttz8^cT5Tzd|E^cp1pZFVF<<#@Us(k$W<NpKF_eB^')))

_TASK_RESCUE=True

# Keep demonstrated market commitments while repairing physical prerequisites.
_TASK_PARENT=intent_agent
_TASK_PROXY=make_agent({0:_TASK_ACTIONS})
_TASK_REPORT={'errors':0,'late_input_requests':0}

def task_market_agent(obs,configuration=None):
    if int(obs['step'])==0:
        for key in _TASK_REPORT:_TASK_REPORT[key]=0
    physical=_TASK_PARENT(obs,configuration)
    scheduled=_TASK_PROXY(obs,configuration)
    orders=[list(order) for order in scheduled.get('market',[])]
    if _TASK_RESCUE:
        # Only overdue task input purchases may supplement the demonstrated queue.
        seat=int(obs['player']);stock=_project_stock(obs,[physical['farmer']]+physical['hands'])
        plans=_PLAN[int(obs['step'])//24]['tasks'];state=_STATE[seat];required={}
        for actor in range(min(len(plans),len(obs['farms'][seat]['hands'])+1)):
            pointer=state['pointers'][actor]
            if pointer>=len(plans[actor]):continue
            task=plans[actor][pointer];cmd=task['op']
            if task['hour']>int(obs['step'])%24 or cmd[0]!='PICKUP':continue
            item=cmd[1];q=int(cmd[2]) if len(cmd)>2 else 1
            required[item]=required.get(item,0)+q
        for item,q in required.items():
            planned=sum(int(o[2]) for o in orders if len(o)>=3 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL') and o[1]==item)
            missing=max(0,q-stock.get(item,0)-planned)
            if missing and len(orders)<10:
                orders.append(['BUY_ANIMAL' if item in _ANIMALS else 'BUY_PRODUCT',item,missing])
                _TASK_REPORT['late_input_requests']+=missing
    physical['market']=orders[:10]
    if int(obs['step'])>=718:
        projected=_project_stock(obs,[physical['farmer']]+physical['hands'])
        physical['market']=[['SELL',i,q] for i,q in projected.items() if q>0 and i in _ITEMS][:10]
    return physical

task_market_agent.telemetry=_TASK_REPORT
agent=task_market_agent
kaggle_submission_agent=task_market_agent
