package com.Fancy.Application;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;

public class ShakeListener implements SensorEventListener
{
	private static final int SPEED_SHRESHOLD = 2000;
	private static final int INTERVAL_TIME = 110;

	private SensorManager sensorManager;
	private Sensor sensor;
	private OnShakeListener onShakeListener;
	private Context mContext;

	private float lastX;
	private float lastY;
	private float lastZ;

	private long lastTime;

	public ShakeListener( Context c )
	{
		mContext = c;
		start( );
	}

	public void start( )
	{
		sensorManager = (SensorManager) mContext.getSystemService( Context.SENSOR_SERVICE );
		if ( sensorManager != null ) 
			sensor = sensorManager.getDefaultSensor( Sensor.TYPE_ACCELEROMETER );

		if ( sensor != null )
			sensorManager.registerListener( this, sensor, SensorManager.SENSOR_DELAY_GAME );
	}

	public void stop( )
	{
		sensorManager.unregisterListener( this );
	}

	public void setOnShakeListener( OnShakeListener listener ) 
	{
		onShakeListener = listener;
	}

	public void onSensorChanged( SensorEvent event ) 
	{
		long currentTime = System.currentTimeMillis( );
		long timeInterval = currentTime - lastTime;

		if ( timeInterval < INTERVAL_TIME )
			return;

		lastTime = currentTime;

		float x = event.values[0];
		float y = event.values[1];
		float z = event.values[2];

		float deltaX = x - lastX;
		float deltaY = y - lastY;
		float deltaZ = z - lastZ;

		lastX = x;
		lastY = y;
		lastZ = z;

		double speed = Math.sqrt( deltaX * deltaX + deltaY * deltaY + deltaZ * deltaZ ) / timeInterval * 10000;

		if ( speed >= SPEED_SHRESHOLD )
			onShakeListener.onShake( );
	}

	public void onAccuracyChanged( Sensor sensor, int accuracy )
	{ }

	public interface OnShakeListener 
	{
		public void onShake( );
	}
}
