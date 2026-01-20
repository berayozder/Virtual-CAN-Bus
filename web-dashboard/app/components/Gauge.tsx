"use client";
import React from 'react';

interface GaugeProps {
    value: number;
    max: number;
    label: string;
    unit: string;
    color?: string;
}

export default function Gauge({ value, max, label, unit, color = "#00f0ff" }: GaugeProps) {
    const radius = 80;
    const stroke = 10;
    const normalizedRadius = radius - stroke * 2;
    const circumference = normalizedRadius * 2 * Math.PI;

    // Cap value to max
    const safeValue = Math.min(value, max);
    const strokeDashoffset = circumference - (safeValue / max) * circumference;

    return (
        <div className="flex flex-col items-center justify-center p-4 glass-panel m-2">
            <div className="relative flex items-center justify-center">
                <svg
                    height={radius * 2}
                    width={radius * 2}
                    className="transform -rotate-90"
                >
                    {/* Background Circle */}
                    <circle
                        stroke="rgba(255,255,255,0.1)"
                        strokeWidth={stroke}
                        fill="transparent"
                        r={normalizedRadius}
                        cx={radius}
                        cy={radius}
                    />
                    {/* Progress Circle */}
                    <circle
                        stroke={color}
                        fill="transparent"
                        strokeWidth={stroke}
                        strokeDasharray={circumference + ' ' + circumference}
                        style={{ strokeDashoffset }}
                        strokeLinecap="round"
                        r={normalizedRadius}
                        cx={radius}
                        cy={radius}
                        className="gauge-arc"
                    />
                </svg>
                <div className="absolute flex flex-col items-center">
                    <span className="text-3xl font-bold font-mono tracking-tighter" style={{ color: color }}>
                        {Math.round(value)}
                    </span>
                    <span className="text-xs text-gray-500">{unit}</span>
                </div>
            </div>
            <h3 className="mt-2 text-sm uppercase tracking-widest text-gray-400">{label}</h3>
        </div>
    );
}
