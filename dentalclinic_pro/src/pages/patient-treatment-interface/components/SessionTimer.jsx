import React, { useState, useEffect } from 'react';
import Icon from '../../../components/AppIcon';

const SessionTimer = ({ startTime, isActive }) => {
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    let interval = null;
    
    if (isActive && startTime) {
      interval = setInterval(() => {
        const now = new Date()?.getTime();
        const elapsed = Math.floor((now - startTime?.getTime()) / 1000);
        setElapsedTime(elapsed);
      }, 1000);
    } else {
      setElapsedTime(0);
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [isActive, startTime]);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;

    if (hours > 0) {
      return `${hours}:${minutes?.toString()?.padStart(2, '0')}:${remainingSeconds?.toString()?.padStart(2, '0')}`;
    }
    return `${minutes}:${remainingSeconds?.toString()?.padStart(2, '0')}`;
  };

  const getTimerColor = () => {
    if (!isActive) return 'text-muted-foreground';
    
    if (elapsedTime < 1800) return 'text-success'; // < 30 min
    if (elapsedTime < 3600) return 'text-warning'; // < 60 min
    return 'text-error'; // > 60 min
  };

  return (
    <div className="flex items-center space-x-2">
      <Icon 
        name={isActive ? "Clock" : "ClockOff"} 
        size={16} 
        color={isActive ? "var(--color-success)" : "var(--color-muted-foreground)"}
      />
      <span className={`text-sm font-mono font-medium ${getTimerColor()}`}>
        {isActive ? formatTime(elapsedTime) : '00:00'}
      </span>
      {isActive && (
        <div className="w-2 h-2 bg-success rounded-full animate-pulse" />
      )}
    </div>
  );
};

export default SessionTimer;