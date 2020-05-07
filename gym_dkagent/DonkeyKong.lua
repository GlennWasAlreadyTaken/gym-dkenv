console.log(memory.getmemorydomainlist())
console.log(memory.getcurrentmemorydomain())


-- *************************************** --
-- 	  	      Usual variables  			   --
-- *************************************** --

--
-- Defining constants for tiles
--

-- Height of the ladder on the tile, starting from the top.
local y_ladders = {}

	-- Height when the ladder is on the platform 
for i=0x00,0x05 do y_ladders[0x40+i] = 0 end

 	-- Height when the ladder is under the platform
y_ladders[0x46] = 7
y_ladders[0x47] = 6
y_ladders[0x48] = 5
y_ladders[0x49] = 4
y_ladders[0x4A] = 3
y_ladders[0x4B] = 2



-- Height of the platforms on the tile, starting from the top.
local y_platforms = {}

	-- Height when the ladder is on the platform 
y_platforms[0x40] = 7
y_platforms[0x41] = 5
y_platforms[0x42] = 4
y_platforms[0x43] = 3
y_platforms[0x44] = 2
y_platforms[0x45] = 1

 	-- Height when the ladder is under the platform
for i=0x00,0x05 do y_platforms[0x46+i] = 0 end


local ladders_and_platforms_tiles = {0x40, 0x41, 0x42, 0x43, 0x44, 0x45,
									 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B}

local ladders_tiles = {0x3F}

local platforms_tiles_down = {0x30,
						 --[[, 0x41, 0x42, 0x43, 0x44, 0x45,]]--
						 0x38, 0x39, 0x3A, 0x3B, 0x3C, 0x3D, 0x3E}

y_platforms[0x30] = 0

y_platforms[0x38] = 7
y_platforms[0x39] = 6
y_platforms[0x3A] = 5
y_platforms[0x3B] = 4
y_platforms[0x3C] = 3
y_platforms[0x3D] = 2
y_platforms[0x3E] = 1

local platforms_tiles_up = {0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37}
											
y_platforms[0x31] = 7
y_platforms[0x32] = 6
y_platforms[0x33] = 5
y_platforms[0x34] = 4
y_platforms[0x35] = 3
y_platforms[0x36] = 2
y_platforms[0x37] = 1

-- Sprites

mario_inf1 = 0x00
mario_sup1 = 0x0F

mario_inf2 = 0x10
mario_sup2 = 0x1F

mario_inf3 = 0x20
mario_sup3 = 0x2F

mario_inf4 = 0x60
mario_sup4 = 0x6F

-- Enemies
enemy_inf1 = 0x80
enemy_sup1 = 0x8F

enemy_inf2 = 0x90
enemy_sup2 = 0x9F

enemy_inf3 = 0xA8
enemy_sup3 = 0xAF

enemy_inf4 = 0xC0
enemy_sup4 = 0xC7

-- Fire coming out of the barrel
enemy_inf5 = 0xFC
enemy_sup5 = 0xFF

moving_platform_inf = 0xA0
moving_platform_sup = 0xA1

-- Hammer
hammer_inf = 0xF6
hammer_sup = 0xFB

-- Colors:
--local purple_color_background = 0x80FF00FF
local purple_color_background = "purple"
--local blue_color_background = 0x800000FF
local blue_color_background = "blue"


-- *************************************** --
-- 	  	      Usual functions  			   --
-- *************************************** --

-- To search a value in an array:
local function has_value (tab, val)
    for index, value in pairs(tab) do
        if value == val then
            return true
        end
    end

    return false
end

-- To split a string:
function string:split(delimiter)
  local result = { }
  local from  = 1
  local delim_from, delim_to = string.find( self, delimiter, from  )
  while delim_from do
    table.insert( result, string.sub( self, from , delim_from-1 ) )
    from  = delim_to + 1
    delim_from, delim_to = string.find( self, delimiter, from  )
  end
  table.insert( result, string.sub( self, from  ) )
  return result
end


-- Prepare client connection to the python server
local host, port = "127.0.0.1", 36297
local tcp = require("lualibs.socket").tcp()
local success, error = tcp:connect(host, port)
if not success then
  print("Failed to connect to server:", error)
  return
end

--tcp:send("bonjour du lua")
--msg = tcp:receive()
--console.log(msg)


-- Resets the environnement and draws the background of the game
-- todo ? it exists several layers of drawings
-- function resetEnv


local minMarioY = 0

-- *************************************** --
-- 	  	          Main Loop   			   --
-- *************************************** --
while true do
	
	

	-- *************************************** --
	-- 	 Receving the command from the server  --
	-- *************************************** --	
	local message, error
	  message, error, receive_buffer = tcp:receive("*l", receive_buffer)
  	if message == nil then
    	if error ~= "timeout" then
      		print("Receive failed: ", error); break
    	end
	else
		-- If the server ask us to reset, we load the checkpoint save
		if message == "RESET" then
			savestate.loadslot(1)
			console.log("reset the save")
			emu.frameadvance()

			minMarioY = memory.read_u8(0x0047) -- we set the minMarioY to the marioY pos value.

		else
			action = message:split(':')
			--[[ Controls:
				"P1 A"
				"P1 B"
				"P1 Down"
				"P1 Left"
				"P1 Right"
				"P1 Select"
				"P1 Start"
				"P1 Up"
				"Power"
				"Reset"
			]]--

			-- We get the control table
			controlTable = joypad.get()
			
			-- If the server wants the A button to be pressed, we mark it as pressed in the control table
			controlTable["P1 A"] = (action[2] == "1")

			-- We do the same with directions:
			direction = action[1]
			if direction == "1" then
				controlTable["P1 Left"] = true
				--console.log("left")
			elseif direction == "2" then
				controlTable["P1 Right"] = true
				--console.log("right")
			elseif direction == "3" then
				controlTable["P1 Up"] = true
				--console.log("up")
			elseif direction == "4" then
				controlTable["P1 Down"] = true
				--console.log("down")
			end

			-- Lastly, we set the control table.
			joypad.set(controlTable)
		end
	
		emu.frameadvance()
		
		--gui.clearGraphics()
		-- *************************************** --
		-- 	  Preparing the informations to send   --
		-- *************************************** --

		local reward = 0
		marioX = memory.read_u8(0x0046)

		marioY = memory.read_u8(0x0047)

		--console.log(marioY)
		if marioY < minMarioY then 
			minMarioY = marioY
			reward = 0.5
		end



		-- If mario is dead, or has won, the level is considered done
		local done = 0
		if memory.read_u8(0x0096) == 255 then 	-- if mario dies
			done = 1 
			reward = -1000
		elseif memory.read_u8(0x0053) ~= 1 then		-- if mario wins (the adress contains the level number) 
			done = 0
			reward = 1000
		end

		


		objX = memory.read_u8(0x0048)
		objY = memory.read_u8(0x0049)

		local widthBox = 7
		--gui.drawBox(marioX, marioY, marioX+widthBox, marioY+widthBox, "white", 0x80FFFFFF)
		--gui.drawBox(objX, objY, objX+widthBox, objY+widthBox, "white", 0x80FFFFFF)
		--gui.drawBox(marioX, marioY, marioX+widthBox, marioY+widthBox, "red", 0x80FF0000)



		memory.usememorydomain("CIRAM (nametables)")
		
		gui.drawBox(0, 0, 256, 239, "black", "black")
		
		-- Looking for the background (platforms, ladders, etc)
		for i=0x000,0x039F do
			-- We read the tile value
			local tile = memory.read_u8(0x0000+i)

			-- We get the position of the tile based on its offset
			local x = (i % 32) * 8
			local y = math.floor(i / 32) * 8

			-- TODO : else of using "has_value", write conditions like x < tile < y


			-- If it's a platform from down
			if has_value(platforms_tiles_down,tile) then
				local yp = y_platforms[tile]

				gui.drawBox(x, y+yp, x+widthBox, y+7, "purple", purple_color_background)

			-- If it's a platform from up
			elseif has_value(platforms_tiles_up,tile) then
				local yp = y_platforms[tile]

				gui.drawBox(x, y, x+widthBox, y+yp-1, "purple", purple_color_background)

			elseif has_value(ladders_tiles, tile) then
				gui.drawBox(x, y, x+widthBox, y+widthBox, "blue", blue_color_background)

			elseif has_value(ladders_and_platforms_tiles, tile) then

				local yl = y_ladders[tile]
				local yp = y_platforms[tile]

				-- If ladder is on the platform
				if yl < yp then

					gui.drawBox(x, y, x+widthBox, y+yp-1, "blue", blue_color_background)
					gui.drawBox(x, y+yp, x+widthBox, y+8, "purple", purple_color_background)

				-- Else, the ladder	is under the platform
				else

					gui.drawBox(x, y, x+widthBox, y+yl-1, "purple", purple_color_background)
					gui.drawBox(x, y+yl, x+widthBox, y+8, "blue", blue_color_background)

				end
			else
				--[[gui.drawBox(x, y, x+widthBox, y+widthBox, "white", 0x50FFFFFF)]]--
			end
		end

		-- Looking for objects in the scene
		memory.usememorydomain("System Bus")
		for i=0,64 do
			local offset = 4 * i
			
			-- Retrieving the points of the sprites
			local upleftx = memory.read_u8(0x0203+offset)
			local uplefty = memory.read_u8(0x0200+offset)
			local sprite = memory.read_u8(0x0201+offset)



			local color = "white"
			--local background_color = 0x80FFFFFF
			local background_color = "white"
			
			if 	mario_inf1 <= sprite and sprite <= mario_sup1
			or 	mario_inf2 <= sprite and sprite <= mario_sup2
			or 	mario_inf3 <= sprite and sprite <= mario_sup3
			or 	mario_inf4 <= sprite and sprite <= mario_sup4 then

				color = "yellow"
				--background_color = 0x80FFFF00
				background_color = "yellow"
				
			elseif  enemy_inf1 <= sprite and sprite <= enemy_sup1
				or 	enemy_inf2 <= sprite and sprite <= enemy_sup2
				or 	enemy_inf3 <= sprite and sprite <= enemy_sup3
				or 	enemy_inf4 <= sprite and sprite <= enemy_sup4
				or 	enemy_inf5 <= sprite and sprite <= enemy_sup5 then

				color = "red"
				--background_color = 0x80FF0000
				background_color = "red"
			
			elseif moving_platform_inf <= sprite and sprite <= moving_platform_sup then

				color = "purple"
				--background_color = purple_color_background
				background_color = "purple"


			elseif hammer_inf <= sprite and sprite <= hammer_sup then
				color = "green"
				--background_color = 0x80FFFF00
				background_color = "green"

			end



			-- Drawing the box around the sprites
			gui.drawBox(upleftx, uplefty, upleftx+widthBox, uplefty+widthBox+1, color, background_color)
			
		end

		gui.DrawFinish()
		--console.log("ready to take screenshot")
		--local marioStat = memory.read_u8(0x0096)

		local path = "D:/INGE_INFO_ANNEE_3/IA_Jeux/DKAgent/screenshots/frame.png"
		client.screenshot(path)
		-- Sending information to the Python script so it can return the controls to perform:
		tcp:send("DKMSG:.:" .. path .. ":.:" .. reward .. ":.:" .. done)
	end
end

tcp:close()
