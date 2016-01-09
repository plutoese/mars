
/**
 * @author plutoese <glen.zhang7@gmail.com>
 * @version 1.0
 * @dick pick
 * @dependency
 * @plugin：
 * @Pikaday：https://github.com/dbushell/Pikaday
 * @Moment.js：http://momentjs.com/
 */

var start_picker = new Pikaday(
{
    field: document.getElementById('startpick'),
    firstDay: 1,
    minDate: new Date(2000, 0, 1),
    maxDate: moment().toDate(),
    yearRange: [2000,2020],
    onSelect: function() {
        end_picker.setMinDate(this.getMoment())
    }
});

var end_picker = new Pikaday(
{
    field: document.getElementById('endpick'),
    firstDay: 1,
    minDate: new Date(2000, 0, 1),
    maxDate: moment().toDate(),
    yearRange: [2000,2020],
    onSelect: function() {
        start_picker.setMaxDate(this.getMoment())
    }
});



