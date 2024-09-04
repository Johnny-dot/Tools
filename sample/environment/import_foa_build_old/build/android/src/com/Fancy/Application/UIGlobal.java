package com.Fancy.Application;

import android.app.Activity;
import android.app.AlertDialog;
import android.os.Message;
import android.text.TextWatcher;
import android.view.Display;
import android.view.SurfaceView;
import android.view.ViewGroup.LayoutParams;
import android.view.ViewTreeObserver.OnGlobalLayoutListener;
import android.widget.AbsoluteLayout;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RelativeLayout;

public class UIGlobal
{
	public static int LUA_UI_INPUT_HEIGHT	= 50;
	public static int LUA_UI_DONE_WIDTH		= 80;

	public final static int SET_X					= 0001;
	public final static int SET_Y					= 0002;
	public final static int SET_W					= 0003;
	public final static int SET_H					= 0004;
	public final static int SET_ENABLE				= 0005;
	public final static int SET_SHOW				= 0006;
	public final static int SET_TOP					= 0007;

	public final static int BUTTON					= 0010;
	public final static int BUTTON_CLICK			= 0011;
	public final static int BUTTON_IMAGE			= 0012;
	public final static int BUTTON_TITLE			= 0013;
	public final static int BUTTON_TITLE_COLOR		= 0014;
	public final static int BUTTON_TITLE_SIZE		= 0015;
	public final static int BUTTON_BACKGROUND_COLOR	= 0016;
	public final static int BUTTON_REMOVE			= 0017;

	public final static int SPIN					= 0020;
	public final static int SPIN_POS				= 0021;
	public final static int SPIN_VALUE				= 0023;
	public final static int SPIN_IMAGE				= 0024;
	public final static int SPIN_SHOW				= 0025;
	public final static int SPIN_REMOVE				= 0026;

	public final static int EDIT					= 0030;
	public final static int EDIT_SET_TEXT			= 0031;
	public final static int EDIT_SET_TEXTSIZE		= 0032;
	public final static int EDIT_SET_TEXTCOLOR		= 0033;
	public final static int EDIT_PASSWORD			= 0034;
	public final static int EDIT_IMAGE				= 0035;
	public final static int EDIT_REMOVE				= 0036;

	public final static int LABEL					= 0040;
	public final static int LABEL_TEXT_SIZE			= 0041;
	public final static int LABEL_TEXT_COLOR		= 0042;
	public final static int LABEL_BACKGROUND_COLOR	= 0043;
	public final static int LABEL_TEXT				= 0044;

	public final static int CHECKBOX				= 0050;
	public final static int CHECKBOX_TITLE			= 0051;
	public final static int CHECKBOX_IMAGE			= 0052;
	public final static int CHECKBOX_REMOVE			= 0053;

	public final static int PANEL					= 0060;
	public final static int PANEL_IMAGE				= 0061;
	public final static int PANEL_REMOVE			= 0062;

	public final static int TILELIST				= 0070;
	public final static int TILELIST_TEXT_SIZE		= 0071;
	public final static int TILELIST_PUSH			= 0072;
	public final static int TILELIST_CLEANUP		= 0073;
	public final static int TILELIST_INVALIDDATE	= 0074;

	public final static int TEXTAREA				= 0100;
	public final static int TEXTAREA_TEXT			= 0101;
	public final static int TEXTAREA_IMAGE			= 0102;
	public final static int TEXTAREA_TEXTSIZE		= 0103;
	public final static int TEXTAREA_TEXTCOLOR		= 0104;
	public final static int TEXTAREA_ALIGN			= 0105;
	public final static int TEXTAREA_REMOVE			= 0106;
	public final static int TEXTAREA_EDITABLE		= 0107;

	public final static int VIDEO					= 0201;
	public final static int VIDEO_PLAY				= 0202;
	public final static int VIDEO_PAUSE				= 0203;
	public final static int VIDEO_LOOP				= 0204;
	public final static int VIDEO_STOP				= 0205;
	public final static int VIDEO_RELEASE			= 0206;
	
	public final static int GFX_EDIT				= 0110;
	public final static int GFX_GET_FOCUS			= 0111;
	
	public final static int LUA_UI_INIT_EDIT		= 0120;
	public final static int LUA_UI_SHOW_EDIT		= 0121;
	public final static int LUA_UI_HIDE_EDIT		= 0122;
	public final static int LUA_UI_REMOVE_EDIT		= 0123;

	public final static int PROMPT					= 0130;

	public static MainActivity active				= null;
	public static FancyGLSurface glView			= null;

	public static AbsoluteLayout layout			= null;
	public static AbsoluteLayout glLayout		= null;
	public static ArrayAdapter<String> mAdapter	= null;
	public static UIMsgHandler handler			= null;
	public static AlertDialog gfx_edit			= null;
	public static EditText inputView			= null;
	public static String text					= "";
	public static String inputViewTitle			= "";
	public static String inputViewCancelBar		= "";
	public static String inputViewDoneBar		= "";
	public static boolean password				= false;
	public static RelativeLayout relativeLayout	= null;
	public static EditText uiInput				= null;
	public static Button btnDone				= null;
	public static TextWatcher textWatcher		= null;
	public static SurfaceView videoview		= null;
	public static int keyboardHeight			= 0;
	public static int x1						= 0;
	public static int y1						= 0;
	public static int x2						= 0;
	public static int y2						= 0;
	public static OnGlobalLayoutListener globalLayoutListener	= null;

	public static void CreateLayout( Activity act )
	{
		UIGlobal.layout =  new AbsoluteLayout( act );
		Display display = act.getWindowManager( ).getDefaultDisplay( );
		act.addContentView( UIGlobal.layout, new LayoutParams( display.getWidth( ), display.getHeight( ) ) );
	}

	public static void sendMessage( Object obj, int what )
	{
		Message message = UIGlobal.handler.obtainMessage( );
		message.what = what;
		message.obj = obj;
		message.sendToTarget( );
	}
}