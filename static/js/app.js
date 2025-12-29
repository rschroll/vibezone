window.onload = function() {
    // Set from timezone to user's current timezone
    const userTZ = Intl.DateTimeFormat().resolvedOptions().timeZone;
    document.getElementById('from_timezone').value = userTZ;

    // Set start and end datetime to next top of the hour and one hour later
    const now = new Date();
    const nextHour = new Date(now);
    nextHour.setHours(now.getHours() + 1, 0, 0, 0);
    const hourAfter = new Date(nextHour);
    hourAfter.setHours(nextHour.getHours() + 1);

    // Format for datetime-local (YYYY-MM-DDTHH:MM)
    const formatDateTime = (date) => {
        return date.toISOString().slice(0, 16);
    };

    document.getElementById('start_datetime').value = formatDateTime(nextHour);
    document.getElementById('end_datetime').value = formatDateTime(hourAfter);

    // Filter timezone options based on search input
    document.getElementById('tz_search').addEventListener('input', function() {
        const filter = this.value.toLowerCase();
        const options = document.querySelectorAll('#to_timezones option');
        options.forEach(option => {
            const show = option.value.toLowerCase().includes(filter);
            option.style.display = show ? '' : 'none';
        });
    });
};
