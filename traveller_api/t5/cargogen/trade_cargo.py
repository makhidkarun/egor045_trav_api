'''cargogen.py'''

from random import seed, randint
import json
import logging
from T5_worldgen.planet import Planet

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)


class FluxRoll(object):
    '''Flux roll'''

    def __init__(self):
        self.die1 = randint(1, 6)
        self.die2 = randint(1, 6)

    def roll(self):
        '''Roll d6 - d6'''
        return self.die1 - self.die2

    def __str__(self):
        return '<die1: {} die2 {}>'.format(
            self.die1, self.die2)


FLUX = FluxRoll()


class TradeCargo(object):
    '''Spec cargo object'''

    def __init__(self):
        self.cost = 0
        self.description = ''
        self.interesting_trade_codes = []
        self.actual_value = 0
        self.price = 0
        self._codes = {
            'Ga': [
                ['Bulk Protein', 'Bulk Carbs', 'Bulk Fats',
                 'Bulk Pharma', 'Livestock', 'Seedstock'],
                ['Flavored Waters', 'Wines', 'Juices',
                 'Nectars', 'Decoctions', 'Drinkable Lymphs'],
                ['Health Foods', 'Nutraceuticals', 'Fast Drug',
                 'Painkillers', 'Antiseptic', 'Antibiotics'],
                ['Incenses', 'Iridescents', 'Photonics',
                 'Pigments', 'Noisemakers', 'Soundmakers'],
                ['Fine Furs', 'Meat Delicacies', 'Fruit Delicacies',
                 'Candies', 'Textiles', 'Exotic Sauces'],
                ['_As', '_De', '_Fl', '_Ic', '_Na', '_In']],
            'Fa': [
                ['Bulk Woods', 'Bulk Pets', 'Bulk Herbs',
                 'Bulk Spices', 'Bulk Nitrates', 'Foodstuffs'],
                ['Flowers', 'Aromatics', 'Pheromones',
                 'Secretions', 'Adhesives', 'Novel Flavorings'],
                ['Antifungals', 'Antivirals', 'Panacea',
                 'Pseudomones', 'Anagathics', 'Slow Drug'],
                ['Strange Seeds', 'Motile Plants', 'Reactive Plants',
                 'IR Emitters', 'Lek Emitters'],
                ['Spices', 'Organic Gems', 'Flavorings',
                 'Aged Meats', 'Fermented Fluids', 'Fine Aromatics'],
                ['_Po', '_Ri', '_Va', '_Ic', '_Na', '_In']],
            'As': [
                ['Bulk Nitrates', 'Bulk Carbon', 'Bulk Iron',
                 'Bulk Copper', 'Radioactive Ores', 'Bulk Ices'],
                ['Ores', 'Ices', 'Carbons',
                 'Metals', 'Uranium', 'Chelates'],
                ['Platinum', 'Gold', 'Gallium',
                 'Silver', 'Thorium', 'Radium'],
                ['Unusual Rocks', 'Fused Metals', 'Strange Crystals',
                 'Fine Dusts', 'Magnetics', 'Light-Sensitives'],
                ['Gemstones', 'Alloys', 'Iridium Sponge',
                 'Lanthanum', 'Isotopes', 'Anti-Matter'],
                ['_Ag', '_De', '_Na', '_Po', '_Ri', '_Ic']],
            'De': [
                ['Bulk Nitrates', 'Bulk Minerals', 'Bulk Abrasives',
                 'Bulk Particulates', 'Exotic Fauna', 'Exotic Flora'],
                ['Archeologicals', 'Fauna', 'Flora',
                 'Minerals', 'Ephemerals', 'Polymers'],
                ['Stimulants', 'Bulk Herbs', 'Palliatives',
                 'Pheromones', 'Antibiotics', 'Combat Drug'],
                ['Envirosuits', 'Reclamation Suits', 'Navigators',
                 'Dupe Masterpieces', 'ShimmerCloth', 'ANIFX Blocker'],
                ['Excretions', 'Flavorings', 'Nectars',
                 'Pelts', 'ANIFX Dyes', 'Seedstock'],
                ['Pheromones', 'Artifacts', 'Sparx',
                 'Repulsant', 'Dominants', 'Fossils']],
            'Fl': [
                ['Bulk Carbon', 'Bulk Petros', 'Bulk Precipitates',
                 'Exotic Fluids', 'Organic Polymers', 'Bulk Synthetics'],
                ['Archeologicals', 'Fauna', 'Flora',
                 'Germanes', 'Flill', 'Chelates'],
                ['Antifungals', 'Antivirals', 'Palliatives',
                 'Counter-prions', 'Antibiotics', 'Cold Sleep Pills'],
                ['Silanes', 'Lek Emitters', 'Aware Blockers',
                 'Soothants', 'Self-Solving Puzzlies', 'Fluidic Timepieces'],
                ['Flavorings', 'Unusual Fluids', 'Encapsulants',
                 'Insidiants', 'Corrosives', 'Exotic Aromatics'],
                ['_In', '_Ri', '_Ic', '_Na', '_Ag', '_Po']],
            'Ic': [
                ['Bulk Ices', 'Bulk Precipitates', 'Bulk Ephemerals',
                 'Exotic Flora', 'Bulk Gases', 'Bulk Oxygen'],
                ['Archeologicals', 'Fauna', 'Flora',
                 'Minerals', 'Luminescents', 'Polymers'],
                ['Antifungals', 'Antivirals', 'Palliatives',
                 'Counter-prions', 'Antibiotics', 'Cold Sleep Pills'],
                ['Silanes', 'Lek Emitters', 'Aware Blockers',
                 'Soothants', 'Self-Solving Puzzlies', 'Fluidic Timepieces'],
                ['Unusual Ices', 'Cryo Alloys', 'Rare Minerals',
                 'Unusual Fluids', 'Cryogems', 'VHDUS Dyes'],
                ['Fossils', 'Cryogems', 'Vision Suppressant',
                 'Fission Suppressant', 'Wafers', 'Cold Sleep Pills']],
            'In': [
                ['Electronics', 'Photonics', 'Magnetics',
                 'Fluidics', 'Polymers', 'Gravitics'],
                ['Obsoletes', 'Used Goods', 'Reparables',
                 'Radioactives', 'Metals', 'Sludges'],
                ['Biologics', 'Mechanicals', 'Textiles',
                 'Weapons', 'Armor', 'Robots'],
                ['Nostrums', 'Restoratives', 'Palliatives',
                 'Chelates', 'Antidotes', 'Antitoxins'],
                ['Software', 'Databases', 'Expert Systems',
                 'Upgrades', 'Backups', 'Raw Sensings'],
                ['Disposables', 'Respirators', 'Filter Masks',
                 'Combination', 'Parts', 'Improvements']],
            'Na': [
                ['Bulk Abrasives', 'Bulk Gases', 'Bulk Minerals',
                 'Bulk Precipitates', 'Exotic Fauna', 'Exotic Flora'],
                ['Archeologicals', 'Fauna', 'Flora',
                 'Minerals', 'Ephemerals', 'Polymers'],
                ['Branded Tools', 'Drinkable Lymphs', 'Strange Seeds',
                 'Pattern Creators', 'Pigments', 'Warm Leather'],
                ['Hummingsand', 'Masterpieces', 'Fine Carpets',
                 'Isotopes', 'Pelts', 'Seedstock'],
                ['Masterpieces', 'Unusual Rocks', 'Artifacts',
                 'Non-fossil Carcasses', 'Replicating Clays', 'ANIFX EMitter'],
                ['_Ag', '_Ri', '_In', '_Ic', '_De', '_Fl']],
            'Po': [
                ['Bulk Nutrients', 'Bulk Fibers', 'Bulk Organics',
                 'Bulk Minerals', 'Bulk Textiles', 'Exotic Flora'],
                ['Art', 'Recordings', 'Writings',
                 'Tactiles', 'Osmancies', 'Wafers'],
                ['Strange Crystals', 'Strange Seeds', 'Pigments',
                 'Emotion Lighting', 'Silanes', 'Flora'],
                ['Gemstones', 'Antiques', 'Collectibles',
                 'Allotropes', 'Spices', 'Seedstock'],
                ['Masterpieces', 'Exotic Flora', 'Antiques',
                 'Incomprehensibles', 'Fossils', 'VHDUS Emitter'],
                ['_In', '_Ri', '_Fl', '_Ic', '_Ag', '_Va']],
            'Ri': [
                ['Bulk Foodstuffs', 'Bulk Protein', 'Bulk Carbs',
                 'Bulk Fats', 'Exotic Flora', 'Exotic Fauna'],
                ['Echostones', 'Self-Defenders', 'Attractants',
                 'Sophont Cuisine', 'Sophone Hats', 'Variable Tattoos'],
                ['Branded Foods', 'Branded Drinks', 'Branded Clothes',
                 'Flavored Drinks', 'Flowers', 'Music'],
                ['Delicacies', 'Spices', 'Tisanes',
                 'Nectars', 'Pelts', 'Variable Tattoos'],
                ['Antique Art', 'Masterpieces', 'Artifacts',
                 'Fine Art', 'Meson Barriers', 'Famous Wafers'],
                ['Edutainments', 'Recordings', 'Writings',
                 'Tactiles', 'Osmancies', 'Wafers']],
            'Va': [
                ['Bulk Dusts', 'Bulk Minerals', 'Bulk Metals',
                 'Radioactive Ores', 'Bulk Particulates', 'Ephererals'],
                ['Branded Vacc Suits', 'Awareness Pinger', 'Strange Seeds',
                 'Pigments', 'Unusual Minerals', 'Exotic Crystals'],
                ['Branded Oxygen', 'Vacc Suit Scents', 'Vacc Suit Patches',
                 'Branded Tools', 'Holo-Companions', 'Flavored Air'],
                ['Vacc Gems', 'Unusual Dusts', 'Insulants',
                 'Crafted Devices', 'Rare Minerals', 'Catalysts'],
                ['Archeologicals', 'Fauna', 'Flora',
                 'Minerals', 'Ephemerals', 'Polymers'],
                ['Obsoletes', 'Used Goods', 'Reparables',
                 'Plutonium', 'Metals', 'Sludges']],
            'Cp': [
                ['Software', 'Expert Systems', 'Databases',
                 'Upgrades', 'Backups', 'Raw Sensings'],
                ['Incenses', 'Contemplatives', 'Cold Welders',
                 'Polymer Sheets', 'Hats', 'Skin Tones'],
                ['Branded Clothes', 'Branded Devices', 'Flavored Drinks',
                 'Flavorings', 'Decorations', 'Group Symbols'],
                ['Monumental Art', 'Holo Sculpture', 'Collectible Books',
                 'Jewelry', 'Museum Items', 'Monumental Art'],
                ['Coinage', 'Currency', 'Money Cards',
                 'Gold', 'Silver', 'Platinum'],
                ['Regulations', 'Synchronzations', 'Expert Systems',
                 'Educationals', 'Mandates', 'Accountings']]
        }
        self.source_world = Planet()
        self.market_world = None
        self.actual_value_rolls = (None, None)
        self.broker_skill = None
        self.broker_dm = None
        self.commission = 0
        self.net_actual_value = 0
        seed()

    def generate_cargo(self, source_uwp, market_uwp=None, broker_skill=0):
        '''Generate cargo'''
        try:
            self.source_world._load_uwp(source_uwp)     # noqa
        except ValueError:
            raise ValueError('Invalid source UWP {}'.format(source_uwp))
        self.broker_skill = broker_skill
        self.source_world.mainworld_type = None
        self.source_world.determine_trade_codes()
        self.source_world.trade_codes = self.purge_ce_trade_codes(
            self.source_world.trade_codes)
        self.description = self.select_cargo_name()
        self.determine_cost(self.source_world.trade_codes)
        self.add_detail(self.source_world.trade_codes)

        if market_uwp is not None:
            self.market_world = Planet()
            try:
                self.market_world._load_uwp(market_uwp)     # noqa
            except ValueError:
                raise ValueError('Invalid market UWP {}'.format(market_uwp))
            self.market_world.mainworld_type = None
            self.market_world.determine_trade_codes()
            self.market_world.trade_codes = self.purge_ce_trade_codes(
                self.market_world.trade_codes
            )
            self.determine_price()

    def select_cargo_name(self, add_detail_flag=True):
        '''Select cargo based on [trade_codes]'''
        # Pick trade code at random
        LOGGER.debug(
            'Supplied trade codes = %s', self.source_world.trade_codes)
        if self.source_world.trade_codes == []:
            LOGGER.debug('No trade codes supplied, using Na')
            trade_code = 'Na'
        else:
            trade_code = self.source_world.trade_codes[randint(
                0, len(self.source_world.trade_codes) - 1)]
        LOGGER.debug('Selected trade code %s', trade_code)

        # Ag => pick either Ga or Fa at random
        if trade_code == 'Ag':
            LOGGER.debug('Trade code is Ag, select either Ga or Fa')
            trade_code = ('Fa' if randint(0, 1) else 'Ga')
            LOGGER.debug('Trade code is %s', trade_code)

        # Validate trade code -- use Na if it's not in the list
        if trade_code not in self._codes:
            LOGGER.debug(
                '%s not in supported trade codes, using Na instead',
                trade_code)
            trade_code = 'Na'

        # Pick cargo at random
        LOGGER.debug('Picking cargo description for %s', trade_code)
        cargo = self._codes[trade_code][randint(0, 5)][randint(0, 5)]
        LOGGER.debug('Selected %s', cargo)

        # Deal with imbalance results (_Xx)
        if cargo.startswith('_'):
            LOGGER.debug('Imbalance cargo %s', cargo)
            add_detail_flag = False
            code = cargo.replace('_', '')
            LOGGER.debug('Rerunning with imbalance')
            cargo = self.select_cargo_name([code])

        # Classification-specific prefix
        prefix = None
        if add_detail_flag:
            prefix = self.add_detail([trade_code])
        if prefix:
            cargo = '{} {}'.format(prefix, cargo)
        return cargo

    @staticmethod
    def add_detail(trade_codes):
        '''Add detail prefix based on trade code'''
        LOGGER.debug('Supplied trade_codes = %s', trade_codes)
        prefixes = {
            'As': 'Strange', 'Ba': 'Gathered', 'De': 'Mineral',
            'Di': 'Artifact', 'Fl': 'Unusual', 'Ga': 'Premium',
            'He': 'Strange', 'Hi': 'Processed', 'Ic': 'Cryo',
            'Ni': 'Unprocessed', 'Po': 'Obscure', 'Ri': 'Quality',
            'Va': 'Exotic', 'Wa': 'Infused'}

        descriptions = []
        for code in trade_codes:
            LOGGER.debug('Processing code %s', code)
            if code in prefixes:
                LOGGER.debug(
                    'Found description %s for code %s', prefixes[code], code)
                descriptions.append(prefixes[code])
        LOGGER.debug('Available descriptions = %s', descriptions)

        # Weed out In/Processed
        if 'Processed' in descriptions and 'In' in trade_codes:
            descriptions.remove('Processed')
        # Weed out As/Exotic
        if 'Exotic' in descriptions and 'As' in trade_codes:
            descriptions.remove('Exotic')

        # Pick one
        if descriptions:
            resp = descriptions[randint(0, len(descriptions) - 1)]
        else:
            resp = None
        return resp

    def determine_cost(self, trade_codes):
        ''' Process trade codes - add valid TCs to self.trade_codes'''
        cost_mods = {
            'Ag': -1000, 'As': -1000, 'Ba': +1000, 'De': +1000,
            'Fl': +1000, 'Hi': -1000, 'Ic': 0, 'In': -1000,
            'Lo': +1000, 'Na': 0, 'Ni': +1000, 'Po': -1000,
            'Ri': +1000, 'Va': +1000
        }
        self.cost = 3000
        self.cost += 100 * int(self.source_world.tech_level)
        LOGGER.debug('Cost = %s', self.cost)
        if trade_codes == []:
            trade_codes = ['Na']
        valid_trade_codes = []
        for trade_code in trade_codes:
            if trade_code in cost_mods.keys():
                LOGGER.debug('Adding trade code %s', trade_code)
                valid_trade_codes.append(trade_code)
            else:
                LOGGER.debug('Ignoring trade code %s', trade_code)
        self.interesting_trade_codes = sorted(list(set(valid_trade_codes)))

        # Add cost modifiers
        for trade_code in self.interesting_trade_codes:
            LOGGER.debug(
                'Processing trade code %s (cost mod = Cr %s)',
                trade_code,
                cost_mods[trade_code])
            self.cost += cost_mods[trade_code]

    def determine_price(self):
        '''Determine price based on source TCs, market TCs'''
        market_mods = {
            'Ag': (['Ag', 'As', 'De', 'Hi', 'In', 'Ri', 'Va'], 1000),
            'As': (['As', 'In', 'Ri', 'Va'], 1000),
            'Ba': (['In'], 1000),
            'De': (['De'], 1000),
            'Fl': (['Fl' 'In'], 1000),
            'Hi': (['Hi'], 1000),
            'In': (['Ag', 'As', 'De', 'Fl', 'Hi', 'In', 'Ri', 'Va'], 1000),
            'Na': (['As', 'De', 'Va'], 1000),
            'Po': (['Ag', 'Hi', 'In', 'Ri'], -1000),
            'Ri': (['Ag', 'De', 'Hi', 'In', 'Ri'], 1000),
            'Va': (['As', 'In', 'Va'], 1000)
        }
        self.price = 5000
        # Market trade codes
        for trade_code in self.source_world.trade_codes:
            if trade_code in market_mods.keys():
                for code in market_mods[trade_code][0]:
                    LOGGER.debug(
                        'Checking source TC %s market TC %s',
                        trade_code,
                        code)
                    if code in self.market_world.trade_codes:
                        LOGGER.debug(
                            'Found match: adjustment = %s',
                            market_mods[trade_code][1])
                        self.price += market_mods[trade_code][1]
                    LOGGER.debug('Price = Cr%s', self.price)
        # TL effect
        tl_mod = 0.1 * (
            int(self.source_world.tech_level) -
            int(self.market_world.tech_level))
        LOGGER.debug('Price TL modifier = %s%%', int(100 * tl_mod))
        self.price = int(self.price * (1 + tl_mod))
        if self.price < 0:
            LOGGER.debug('Price (Cr%s) < Cr0, resetting to Cr0', self.price)
            self.price = 0
        LOGGER.debug('Price = %s', self.price)
        self.actual_value = int(self.price * self.determine_actual_value())
        LOGGER.debug('actua value = %s', self.actual_value)
        self.commission = int(0.05 * self.broker_dm * self.price)
        LOGGER.debug('commission = %s', self.commission)
        self.net_actual_value = self.actual_value - self.commission

    def determine_actual_value(self, modifier=0):
        '''Determine actual value using flux roll'''
        broker_dm = int((self.broker_skill + 0.5) / 2)
        broker_dm = min(4, broker_dm)
        self.broker_dm = broker_dm
        flux = FLUX.roll() + modifier + self.broker_dm
        self.actual_value_rolls = (FLUX.die1, FLUX.die2)

        flux = max(-5, flux)
        flux = min(8, flux)

        if flux <= -4:
            actual_value_multiplier = float(9 + flux) / 10.0
        elif flux <= 3 and flux > -4:
            actual_value_multiplier = float(10 + flux) / 10.0
        elif flux <= 5 and flux > 3:
            actual_value_multiplier = float(7 + 2 * flux) / 10.0
        elif flux > 5:
            actual_value_multiplier = float(flux - 4) / 10.0
        LOGGER.debug(
            'flux result = %s flux rolls = +%s -%s ',
            flux,
            self.actual_value_rolls[0], self.actual_value_rolls[1])
        LOGGER.debug(
            'modifier = %s actual_value_multiplier = %s',
            modifier,
            actual_value_multiplier)

        return actual_value_multiplier

    def __str__(self):
        source = '{}-{} Cr{:,} {}'.format(
            self.source_world.tech_level,
            ' '.join(self.interesting_trade_codes),
            self.cost,
            self.description)
        return source

    def json(self):
        '''JSON representation'''
        if self.market_world is not None:
            market_world_trade_codes = self.market_world.trade_codes
            market_world_uwp = self.market_world.uwp()
        else:
            market_world_trade_codes = []
            market_world_uwp = None

        doc = {
            "cargo": str(self),
            "cost": self.cost,
            "description": self.description,
            "market": {
                "trade_codes": market_world_trade_codes,
                "uwp": market_world_uwp,
                "net_actual_value": self.net_actual_value,
                "gross_actual_value": self.actual_value,
                "broker_commission": self.commission
            },
            "price": self.price,
            "source": {
                "trade_codes": self.source_world.trade_codes,
                "uwp": self.source_world.uwp()
            },
            "tech_level": int(self.source_world.tech_level),
            "notes": {
                "actual_value_rolls": self.actual_value_rolls,
                "broker_skill": self.broker_skill
            }
        }
        return json.dumps(doc)

    @staticmethod
    def purge_ce_trade_codes(trade_codes):
        '''Purge CE trade codes'''
        try:
            assert isinstance(trade_codes, list)
        except AssertionError:
            raise ValueError('trade_codes must be type list')
        for indx, code in enumerate(trade_codes):
            if code in ['Ht', 'Lt']:
                del trade_codes[indx]
        return trade_codes
