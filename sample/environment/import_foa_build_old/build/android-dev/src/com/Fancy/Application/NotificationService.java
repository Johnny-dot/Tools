package com.Fancy.Application;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.NoSuchElementException;
import java.util.TreeSet;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.IBinder;

public class NotificationService extends Service
{
	private final int RepeatPerYear		= 2;
	private final int RepeatPerMonth	= 3;
	private final int RepeatPerDay		= 4;
	private final int RepeatPerHour		= 5;
	private final int RepeatPerMinute	= 6;

	private TreeSet<NotifyParam>	mNotification	= null;
	private MessageThread			mThread			= null;
	private Service					mService		= null;

	class NotifyParam implements Comparable<NotifyParam>
	{
		public int		mID;
		public long		mMilliseconds;
		public String	mTitle;
		public String	mContent;
		public int		mType;
		public boolean	mNextEqual;

		public NotifyParam( int id, long milliseconds, String title, String content, int type )
		{
			mID = id;
			mMilliseconds = milliseconds;
			mTitle = title;
			mContent = content;
			mType = type;
			mNextEqual = false;
		}

		@Override
		public int compareTo( NotifyParam another )
		{
			if ( mID == another.mID )
			{
				another.mMilliseconds = mMilliseconds;
				another.mTitle = mTitle;
				another.mContent = mContent;
				another.mType = mType;
				return 0;
			}

			if ( mMilliseconds < another.mMilliseconds )
			{
				return -1;
			}
			else if ( mMilliseconds == another.mMilliseconds )
			{
				another.mNextEqual = true;
				return 1;
			}
			else
			{
				return 1;
			}
		}
	}

	class MessageThread extends Thread
	{
		public boolean isRunning = true;

		@Override
		public void run( )
		{
			super.run( );

			while ( isRunning )
			{
				if ( mNotification.isEmpty( ) )
					continue;

				try
				{
					NotifyParam np = mNotification.first( );
					if ( np.mMilliseconds == -1 )
					{
						mNotification.remove( np );
						continue;
					}

					long currentTime = System.currentTimeMillis( );
					if ( Math.abs( np.mMilliseconds - currentTime ) <= 500  )
					{
						int id = np.mID;
						long millisesconds = np.mMilliseconds;
						String title = np.mTitle;
						String content = np.mContent;
						int type = np.mType;
						NotificationManager nm = (NotificationManager) mService.getSystemService( Context.NOTIFICATION_SERVICE );

						Notification nf = new Notification( R.drawable.ic_launcher, content, millisesconds );
						nf.defaults = Notification.DEFAULT_ALL;
						nf.flags = Notification.FLAG_AUTO_CANCEL;

						Intent it = new Intent( mService, MainActivity.class );
						it.putExtra( "notifyid", id );
						PendingIntent contentIntent = PendingIntent.getActivity( mService, id, it, PendingIntent.FLAG_UPDATE_CURRENT );
						nf.setLatestEventInfo( mService, title, content, contentIntent );

						nm.notify( np.mID, nf );
						mNotification.remove( np );

						if ( type == RepeatPerYear )
							millisesconds += 365 * 24 * 60 * 60 * 1000;
						else if ( type == RepeatPerMonth )
							millisesconds += 30 * 24 * 60 * 60 * 1000;
						else if ( type == RepeatPerDay )
							millisesconds += 24 * 60 * 60 * 1000;
						else if ( type == RepeatPerHour )
							millisesconds += 60 * 60 * 1000;
						else if ( type == RepeatPerMinute )
							millisesconds += 60 * 1000;

						if ( type != -1 )
							mNotification.add( new NotifyParam( id, millisesconds, title, content, type ) );

						if ( np.mNextEqual )
							continue;
					}
					else if ( currentTime - np.mMilliseconds > 500 )
					{
						int type = np.mType;
						if ( type < RepeatPerYear || type > RepeatPerMinute )
							continue;

						long millisesconds = np.mMilliseconds;
						while ( millisesconds + 500 < currentTime )
						{
							if ( type == RepeatPerYear )
								millisesconds += 365 * 24 * 60 * 60 * 1000;
							else if ( type == RepeatPerMonth )
								millisesconds += 30 * 24 * 60 * 60 * 1000;
							else if ( type == RepeatPerDay )
								millisesconds += 24 * 60 * 60 * 1000;
							else if ( type == RepeatPerHour )
								millisesconds += 60 * 60 * 1000;
							else if ( type == RepeatPerMinute )
								millisesconds += 60 * 1000;
						}

						np.mMilliseconds = millisesconds;
					}

				}
				catch ( NoSuchElementException e )
				{
					continue;
				}

				try
				{
					Thread.sleep( 500 );
				}
				catch (InterruptedException e)
				{
					e.printStackTrace();
				}
			}
		}
	}
	
	@Override
	public IBinder onBind( Intent intent )
	{
		// TODO
		return null;
	}

	@Override
	public void onCreate( )
	{
		super.onCreate( );
		if ( mService == null )
			mService = this;

		if ( mNotification == null )
			mNotification = new TreeSet<NotifyParam>( );

		if ( mThread == null )
		{
			mThread = new MessageThread( );
			mThread.start( );
		}
	}

	@Override
	public int onStartCommand( Intent intent, int flags, int startId )
	{
		super.onStartCommand( intent, flags, startId );

		if ( intent.getBooleanExtra( "cancelall", false ) )
		{
			( (NotificationManager) getSystemService( Context.NOTIFICATION_SERVICE ) ).cancelAll( );
			mNotification.clear( );
			mThread.isRunning = false;
			stopSelf( );

			return START_REDELIVER_INTENT;
		}

		if ( intent.getBooleanExtra( "cancel", false ) )
		{
			mNotification.add( new NotifyParam( intent.getIntExtra( "notifyid", -1 ), -1, "", "", 0 ) );
			return START_REDELIVER_INTENT;
		}

		int id = intent.getIntExtra( "notifyid", -1 );
		String title = intent.getStringExtra( "notifytitle" );
		String content = intent.getStringExtra( "notifycontent" );
		int type = intent.getIntExtra( "notifytype", -1 );

		SimpleDateFormat format = new SimpleDateFormat( "yyyy-MM-dd-HH-mm-ss" );
		Date time = null;
		try
		{
			time = format.parse( intent.getStringExtra( "notifydate" ).toString( ) );
			mNotification.add( new NotifyParam( id, time.getTime( ), title, content, type ) );
		} 
		catch ( Exception e )
		{
			e.printStackTrace( );
		}

		return START_REDELIVER_INTENT;		
	}

	@Override
	public void onDestroy( )
	{
		System.out.println("Restart the NotificationService!");
		startService( new Intent( this, NotificationService.class ) );

		super.onDestroy( );
	}
}