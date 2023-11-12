# Mq-Islamic-Local-Prayer-Times

The Mq-Islamic-Local-Prayer-Times is a Home Assistant integration designed to calculate Islamic prayer times locally, without the need for an internet connection. It utilizes the calculations based on the method developed by Dr. Eng. Rinto Anugraha NQZ, S.Si., M.Si. All credit goes to him ( Learn more about [Dr. Rinto Anugraha's calculations](https://rintoanugraha.staff.ugm.ac.id/) ).

This integration is ideal for users who require reliable, locally computed Islamic prayer times for their Home Assistant setup.

# Features
Local Calculation: Computes prayer times locally, ensuring reliability and privacy.
Customizable Settings: Allows adjustments to calculation parameters for increased accuracy specific to your location.

# Configuration
The configuration for the Mq-Islamic-Local-Prayer-Times integration can be completed during the initial installation, or it can be done at a later time. To reconfigure the integration, navigate to the Mq-Islamic-Local-Prayer-Times configuration page and click the 'Configure' button. Here, you will be able to adjust the following parameters:

- Time Zone: Your time zone.

- Latitude: Latitude of your location.

- Longitude: Longitude of your location.

- Elevation: Elevation above sea level in meters.

- Fajr Angle: Angle for Fajr (ussually beetween 15 - 20 degree).

- Dhuha Angle: Angle for Dhuha (ussually beetween 3 - 5 degree).

- Isha Angle: Angle for Isha (night).

- Ikhtiyat Subuh: Safety time for Fajr.

- Ikhtiyat Zuhur: Safety time for Zuhr (noon).

- Ikhtiyat Ashar: Safety time for Asr (afternoon).

- Ikhtiyat Maghrib: Safety time for Maghrib (sunset).

- Ikhtiyat Isya: Safety time for Isha.

# Installation
To install the integration, transfer the Mq-Islamic-Local-Prayer-Times directory along with everything in it to the custom_components directory of your Home Assistant. Typically, this directory can be found within your /config directory. For those using Hass.io, you can employ SAMBA for transferring the directory. In case you're utilizing Home Assistant Supervised, you might find the custom_components directory at /usr/share/hassio/homeassistant. If the custom_components directory doesn't exist, you'll have to create it first before moving the Mq-Islamic-Local-Prayer-Times directory and all included files into this location.

# Usage
The integration creates sensors such as sensor.ashar, sensor.maghrib, and so on. You can utilize these sensors as needed within your Home Assistant.

# Support
For support, issues, or feature requests, please file an issue on the GitHub repository.

# License
This project is licensed under [GNU General Public License v3.0](https://github.com/AndroX55/Mq-Islamic-Local-Prayer-Times/blob/main/LICENSE) - see the LICENSE.md file for details.
