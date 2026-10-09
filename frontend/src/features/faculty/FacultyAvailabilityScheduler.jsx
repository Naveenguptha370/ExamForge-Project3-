import React, { useState } from 'react';
import './schedulerStyles.css';

const DAYS = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'];
const SLOTS = ['09:00 - 12:00', '14:00 - 17:00'];

export function FacultyAvailabilityScheduler({ facultyMember }) {
  const [schedule, setSchedule] = useState({
    'MONDAY-09:00 - 12:00': true,
    'MONDAY-14:00 - 17:00': true,
    'TUESDAY-09:00 - 12:00': true,
    'WEDNESDAY-09:00 - 12:00': false,
    'THURSDAY-14:00 - 17:00': true,
    'FRIDAY-09:00 - 12:00': true,
  });

  const toggleSlot = (day, slot) => {
    const key = `${day}-${slot}`;
    setSchedule(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="ef-scheduler-wrap">
      <div className="ef-scheduler-header">
        <h3 className="ef-sched-title">Weekly Availability Matrix</h3>
        <p className="ef-sched-desc">Configure invigilation slot availability for {facultyMember?.name || 'Selected Faculty'}.</p>
      </div>

      <div className="ef-grid-container">
        <table className="ef-sched-table">
          <thead>
            <tr>
              <th>Day of Week</th>
              {SLOTS.map(s => <th key={s}>{s}</th>)}
            </tr>
          </thead>
          <tbody>
            {DAYS.map(day => (
              <tr key={day}>
                <td className="ef-day-cell">{day}</td>
                {SLOTS.map(slot => {
                  const key = `${day}-${slot}`;
                  const isAvail = !!schedule[key];
                  return (
                    <td key={slot} className="ef-slot-cell">
                      <button
                        onClick={() => toggleSlot(day, slot)}
                        className={`ef-slot-btn ${isAvail ? 'available' : 'unavailable'}`}
                      >
                        {isAvail ? 'Available' : 'Unavailable'}
                      </button>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
