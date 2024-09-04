package com.Fancy.Application;

public class FancyMessage
{
	public final static int _TOUCH_BEGIN			= 0;
	public final static int _EVENT_TOUCH_MOVE		= 1;
	public final static int _EVENT_TOUCH_END		= 2;
	public final static int _EVENT_TOUCH_ZOOM		= 3;
	public final static int _EVENT_ROTATE			= 4;
	public final static int _EVENT_BUTTON_CLICK		= 5;
	public final static int _EVENT_SPIN_PCLICK		= 6;
	public final static int _EVENT_SPIN_NCLICK		= 7;
	public final static int _EVENT_EDIT_CHANGE		= 8;
	public final static int _EVENT_CHECK_SELECT		= 9;
	public final static int _EVENT_TILELIST_CLICK	= 10;
	public final static int _EVENT_GFXEDIT_CHANGE	= 11;
	public final static int _EVENT_BACK_BUTTON 		= 12;
	public final static int _EVENT_ACTIVE_STATE		= 13;
	public final static int _EVENT_SHAKE			= 14;
	public final static int _EVENT_RESIZE			= 15;
	public final static int _EVENT_NOTIFY			= 16;
	public final static int _EVENT_KEYBOARD			= 17;
	public final static int _EVENT_NETCHANGE		= 18;
	public final static int _EVENT_PAYRESULT		= 19;
	public final static int _EVENT_KEYDOWN			= 20;
	public final static int _EVENT_KEYUP			= 21;
	public final static int _EVENT_CHAR				= 22;
	public final static int _EVENT_VISIBLE_TEXTBOX	= 23;
	public final static int _EVENT_RESTORE_TEXTBOX	= 24;
	public final static int _EVENT_SDK_RESULT		= 25;

	public int		mType;
	public int		mWindow;
	public boolean	mIsSelect;
	public boolean	mIsArea;
	public int		mKey;
	public String	mStr;
	public int		mKeyboardHeight;
	public int		mX1;
	public int		mY1;
	public int		mX2;
	public int		mY2;

	public FancyMessage( )
	{
		mType			= -1;
		mWindow			= 0;
		mIsSelect		= false;
		mIsArea			= false;
		mKey			= 0;
		mStr			= "";
		mX1				= 0;
		mY1				= 0;
		mX2				= 0;
		mY2				= 0;
	}
}
