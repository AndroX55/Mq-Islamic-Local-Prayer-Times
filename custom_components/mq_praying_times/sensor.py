import math
from datetime import datetime, timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect, async_dispatcher_send

from .const import SIGNAL_CONFIG_UPDATED, DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up a prayer time sensor based on a config entry."""
    # Use the entry_id to create a unique set of entities per config_entry
    unique_id = config_entry.entry_id

    if unique_id not in hass.data[DOMAIN]:
        # if it doesn't exist in hass.data[DOMAIN]
        hass.data[DOMAIN][unique_id] = []

    # if the entry has already been setup
    if hass.data[DOMAIN][unique_id]:
        return False

    # Create sensor entities based on the config_entry
    sensors = [
        PrayerTimeSensor(config_entry.data, "Subuh"),
        PrayerTimeSensor(config_entry.data, "Dhuha"),
        PrayerTimeSensor(config_entry.data, "Zuhur"),
        PrayerTimeSensor(config_entry.data, "Ashar"),
        PrayerTimeSensor(config_entry.data, "Maghrib"),
        PrayerTimeSensor(config_entry.data, "Isya"),
        PrayerTimeSensor(config_entry.data, "Imsak"),
		PrayerTimeSensor(config_entry.data, "Syuruq"),
		PrayerTimeSensor(config_entry.data, "Last Third")
    ]

    # Add sensor entities
    async_add_entities(sensors)

    # Store the sensors in hass.data
    hass.data[DOMAIN][unique_id] = sensors
    return True

class PrayerTimeSensor(Entity):
    """Representation of a Prayer Time Sensor."""

    def __init__(self, config, prayer_name):
        """Initialize the sensor."""
        self._config = config
        self._name = f"{prayer_name}"
        self._prayer_name = prayer_name
        self._state = None
        
    @property
    def unique_id(self):
        """Return the unique ID."""
        return f"mq_prayer_times_{self._prayer_name}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        # Return the next prayer time
        return self._state
        
    @property
    def icon(self):
        """Return the icon."""
        return 'mdi:mosque-outline'
        
    async def async_added_to_hass(self):
        # Register a callback if config updated
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL_CONFIG_UPDATED, self._handle_config_update
            )
        )

    @callback
    def _handle_config_update(self, new_config):
        # Update the entity's config
        self._config = new_config
        # Apply new configuration
        self.async_schedule_update_ha_state(True)

    async def async_update(self):
        """Fetch new state data."""
        zona = self._config.get('zona')
        lintang = self._config.get('lintang')
        bujur = self._config.get('bujur')
        ketinggian = self._config.get('ketinggian')
        sudut_subuh = self._config.get('sudut_subuh')
        sudut_dhuha = self._config.get('sudut_dhuha')
        sudut_isya = self._config.get('sudut_isya')
        ikhtiyat_subuh = self._config.get('ikhtiyat_subuh')
        ikhtiyat_zuhur = self._config.get('ikhtiyat_zuhur')
        ikhtiyat_ashar = self._config.get('ikhtiyat_ashar')
        ikhtiyat_maghrib = self._config.get('ikhtiyat_maghrib')
        ikhtiyat_isya = self._config.get('ikhtiyat_isya')
        ikhtiyat_syuruq = self._config.get('ikhtiyat_syuruq')
        ikhtiyat_dhuha = self._config.get('ikhtiyat_dhuha')

        # Calculate prayer times
        prayer_times = await self.hass.async_add_executor_job(
		calculate_prayer_times, zona, lintang, bujur, ketinggian, 
		sudut_subuh, sudut_dhuha, sudut_isya, ikhtiyat_subuh, ikhtiyat_zuhur, 
		ikhtiyat_ashar, ikhtiyat_maghrib, ikhtiyat_isya, ikhtiyat_syuruq, ikhtiyat_dhuha
        )

        # Set the state based on the prayer name
        if self._prayer_name == "Subuh":
            self._state = prayer_times['subuh']
        elif self._prayer_name == "Dhuha":
            self._state = prayer_times['dhuha']
        elif self._prayer_name == "Zuhur":
            self._state = prayer_times['zuhur']
        elif self._prayer_name == "Ashar":
            self._state = prayer_times['ashar']
        elif self._prayer_name == "Maghrib":
            self._state = prayer_times['maghrib']
        elif self._prayer_name == "Isya":
            self._state = prayer_times['isya']
        elif self._prayer_name == "Imsak":
            self._state = prayer_times['imsak']
        elif self._prayer_name == "Syuruq":
            self._state = prayer_times['syuruq']
        elif self._prayer_name == "Last Third":
            self._state = prayer_times['last_third']

def calculate_prayer_times(
	zona, lintang, bujur, ketinggian, sudut_subuh, sudut_dhuha, 
	sudut_isya, ikhtiyat_subuh, ikhtiyat_zuhur, ikhtiyat_ashar, ikhtiyat_maghrib, 
	ikhtiyat_isya, ikhtiyat_syuruq, ikhtiyat_dhuha
):

	# Get the current timestamp
	current_time = datetime.now()

	# Calculate the day, month, and year from the timestamp
	tgl = int(current_time.strftime('%-d'))
	bln = int(current_time.strftime('%-m'))
	thn = int(current_time.strftime('%Y'))

	if bln < 3:
		M = bln + 12
		Y = thn - 1
	else:
		M = bln
		Y = thn

	A = round(thn / 100)
	B = (2 - A) + int(A / 4)
	JulianUT = 1720994.5 + (365.25 * Y) + (30.60001 * (M + 1)) + B + tgl + 12 / 24
	JulianLT = JulianUT - zona / 24
	SudutTgl = 2 * math.pi * (JulianLT - 2451545) / 365.25
	U = (JulianLT - 2451545) / 36525
	L0 = (280.46607 + 36000.7698 * U) * math.pi / 180
	Deklinasi = (
		0.37877 
		+ 23.264 * math.sin((57.297 * SudutTgl - 79.547) * math.pi / 180)
		+ 0.3812 * math.sin((2 * 57.297 * SudutTgl - 82.682) * math.pi / 180)
		+ 0.17132 * math.sin((3 * 57.297 * SudutTgl - 59.722) * math.pi / 180)
	)
	EqOfTime = (
		(-1 * (1789 + 237 * U) * math.sin(L0)
		 - (7146 - 62 * U) * math.cos(L0)
		 + (9934 - 14 * U) * math.sin(2 * L0)
		 - (29 + 5 * U) * math.cos(2 * L0)
		 + (74 + 10 * U) * math.sin(3 * L0)
		 + (320 - 4 * U) * math.cos(3 * L0)
		 - 212 * math.sin(4 * L0)
		)
		/ 1000
	)
	DeklinasiRad = Deklinasi * math.pi / 180
	LintangRad = lintang * math.pi / 180
	TransitM = 12 + zona - bujur / 15 - EqOfTime / 60
	Terbit = TransitM - (12 / math.pi) * math.acos(
		(
			math.sin((-0.8333 - 0.0347 * ketinggian ** 0.5) * math.pi / 180) 
			- math.sin(DeklinasiRad) * math.sin(LintangRad)
		) 
		/ (math.cos(DeklinasiRad) * math.cos(LintangRad))
	)

	subuh = (
		ikhtiyat_subuh / 60 
		+ TransitM 
		- (12 / math.pi) * math.acos(
			(math.sin(-1 * sudut_subuh * math.pi / 180) 
			 - math.sin(DeklinasiRad) * math.sin(LintangRad)) 
			/ (math.cos(DeklinasiRad) * math.cos(LintangRad))
		)
	)

	dhuha = (
		ikhtiyat_dhuha / 60
		+ TransitM 
		- (12 / math.pi) * math.acos(
			(math.sin(sudut_dhuha * math.pi / 180) 
			 - math.sin(DeklinasiRad) * math.sin(LintangRad))
			/ (math.cos(DeklinasiRad) * math.cos(LintangRad))
		)
	)

	zuhur = ikhtiyat_zuhur / 60 + TransitM

	ashar = (
		ikhtiyat_ashar / 60 
		+ TransitM 
		+ (12 / math.pi) * math.acos(
			(math.sin(math.atan(1 / (1 + math.tan(abs(LintangRad - DeklinasiRad))))) 
			 - math.sin(DeklinasiRad) * math.sin(LintangRad))
			/ (math.cos(DeklinasiRad) * math.cos(LintangRad))
		)
	)

	maghrib = (
		ikhtiyat_maghrib / 60 
		+ TransitM 
		+ (12 / math.pi) * math.acos(
			(math.sin((-0.8333 - 0.0347 * ketinggian ** 0.5) * math.pi / 180) 
			 - math.sin(DeklinasiRad) * math.sin(LintangRad)) 
			/ (math.cos(DeklinasiRad) * math.cos(LintangRad))
		)
	)

	isya = (
		ikhtiyat_isya / 60 
		+ TransitM 
		+ (12 / math.pi) * math.acos(
			(math.sin(-1 * sudut_isya * math.pi / 180) 
			 - math.sin(DeklinasiRad) * math.sin(LintangRad))
			/ (math.cos(DeklinasiRad) * math.cos(LintangRad))
		)
	)
	imsak = subuh - 10 / 60
	syuruq = Terbit + ikhtiyat_syuruq / 60
	last_third = subuh - (subuh + (24 - maghrib)) / 3
	
	def format_prayer_time(hour_float, round_up=True):
		"""Converts hours into HH:MM format."""
		hours = int(hour_float)
		if round_up:
			minutes = math.ceil((hour_float - hours) * 60) # Round up
		else:
			minutes = math.floor((hour_float - hours) * 60) # Round down

		# Minutes overflow
		if minutes >= 60:
			hours += 1
			minutes -= 60

		return '{:02d}:{:02d}'.format(hours, minutes)

	prayer_times = {
		'subuh': format_prayer_time(subuh),
		'syuruq': format_prayer_time(syuruq, round_up=False),
		'dhuha': format_prayer_time(dhuha),
		'zuhur': format_prayer_time(zuhur),
		'ashar': format_prayer_time(ashar),
		'maghrib': format_prayer_time(maghrib),
		'isya': format_prayer_time(isya),
		'imsak': format_prayer_time(imsak),
		'last_third': format_prayer_time(last_third)
	}

	return prayer_times
