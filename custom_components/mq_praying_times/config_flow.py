import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect, async_dispatcher_send

from .const import SIGNAL_CONFIG_UPDATED
from .const import DOMAIN

class MQPrayingTimesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    data_schema = vol.Schema({
        vol.Required('zona', default=7): vol.Coerce(int),
        vol.Required('lintang', default=4.100319434414599): vol.Coerce(float),
        vol.Required('bujur', default=98.22077370975109): vol.Coerce(float),
        vol.Required('ketinggian', default=1): vol.Coerce(int),
        vol.Required('sudut_subuh', default=20): vol.Coerce(float),
        vol.Required('sudut_dhuha', default=5): vol.Coerce(float),
        vol.Required('sudut_isya', default=18): vol.Coerce(float),
        vol.Required('ikhtiyat_subuh', default=2): vol.Coerce(int),
        vol.Required('ikhtiyat_zuhur', default=3): vol.Coerce(int),
        vol.Required('ikhtiyat_ashar', default=2): vol.Coerce(int),
        vol.Required('ikhtiyat_maghrib', default=2): vol.Coerce(int),
        vol.Required('ikhtiyat_isya', default=2): vol.Coerce(int),
        vol.Required('ikhtiyat_syuruq', default=2): vol.Coerce(int),
        vol.Required('ikhtiyat_dhuha', default=2): vol.Coerce(int),
    })

    async def async_step_user(self, user_input=None):
        existing_entry = next(
            (entry for entry in self._async_current_entries()
             if entry.domain == DOMAIN),
            None
        )

        if existing_entry:
            return self.async_abort(reason="single_instance_allowed")
        
        errors = {}

        if user_input is not None:
            # Validate
            if not -90 <= user_input['lintang'] <= 90:
                errors['lintang'] = 'invalid_latitude'
            if not -180 <= user_input['bujur'] <= 180:
                errors['bujur'] = 'invalid_longitude'

            if not errors:
                # Create the configuration entry
                return self.async_create_entry(title="Mq Prayer Times", data=user_input)

        # If there is no user input or there are errors, show the configuration form again
        return self.async_show_form(
            step_id='user', 
            data_schema=self.data_schema,
            errors=errors
        )
        
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return MQPrayingTimesOptionsFlowHandler(config_entry)

class MQPrayingTimesOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        # Initialize the options flow
        return await self.async_step_options()

    async def async_step_options(self, user_input=None):
        errors = {}
        current_config = self.config_entry.data
        
        # Define the configuration parameters along with their types and default values
        config_params = {
		'zona': int,
		'lintang': float,
		'bujur': float,
		'ketinggian': int,
		'sudut_subuh': float,
		'sudut_dhuha': float,
		'sudut_isya': float,
		'ikhtiyat_subuh': int,
		'ikhtiyat_zuhur': int,
		'ikhtiyat_ashar': int,
		'ikhtiyat_maghrib': int,
		'ikhtiyat_isya': int,
		'ikhtiyat_syuruq': int,
		'ikhtiyat_dhuha': int
        }

        # Build the data schema dynamically based on the config parameters
        data_schema_fields = {
            vol.Required(key, default=current_config.get(key, '')): vol.Coerce(value)
            for key, value in config_params.items()
        }
        data_schema = vol.Schema(data_schema_fields)

        if user_input is not None:
            # Validate
            if not -90 <= user_input['lintang'] <= 90:
                errors['lintang'] = 'invalid_latitude'
            if not -180 <= user_input['bujur'] <= 180:
                errors['bujur'] = 'invalid_longitude'

            if not errors:
            
                # Update the config entry with the new user input
                updated_data = {**current_config, **user_input}
                self.hass.config_entries.async_update_entry(
                    self.config_entry, data=updated_data
                )
                # Notify entities about the update using a dispatcher
                async_dispatcher_send(self.hass, SIGNAL_CONFIG_UPDATED, updated_data)
            
                # No need to create a new entry, just inform the user that the update was successful
                return self.async_abort(reason="configuration_updated")

        # Show the options form
        return self.async_show_form(
            step_id="options",
            data_schema=data_schema,
            errors=errors
        )
