import threading

class LoadCell(threading.Thread):

    def __init__(self,sensor):
        threading.Thread.__init__(self)
        self.hx = sensor
        self.load = 0
        self.bin = ""
        self.initialize()

    def run(self):
        while True:
            self.load = self.hx.get_weight_mean()

            binary=(self.load/0.0119)
            n=int(binary)
            x=n
            k=[]
            while (n>0):
                   a=int(float(n%2))
                   k.append(a)
                   n=(n-a)/2
            k.append(0)
            string=""
            for j in k[::-1]:
                string=string+str(j)
            self.bin = string

    def initialize(self):

        err = self.hx.zero()
        # check if successful
        if err:
            raise ValueError('Tare is unsuccessful.')

        reading = self.hx.get_raw_data_mean()
        if reading:  # always check if you get correct value or only False
            # now the value is close to 0
            print('Data subtracted by offset but still not converted to units:',
                  reading)
        else:
            print('invalid data', reading)

        # In order to calculate the conversion ratio to some units, in my case I want grams,
        # you must have known weight.
        input('Put known weight on the scale and then press Enter')
        reading = self.hx.get_data_mean()
        if reading:
            print('Mean value from HX711 subtracted by offset:', reading)
            known_weight_grams = input(
                'Write how many grams it was and press Enter: ')
            try:
                value = float(known_weight_grams)
                print(value, 'grams')
            except ValueError:
                print('Expected integer or float and I have got:',
                      known_weight_grams)

            # set scale ratio for particular channel and gain which is
            # used to calculate the conversion to units. Required argument is only
            # scale ratio. Without arguments 'channel' and 'gain_A' it sets
            # the ratio for current channel and gain.
            ratio = reading / value  # calculate the ratio for channel A and gain 128
            self.hx.set_scale_ratio(ratio)  # set ratio for current channel
            print('Ratio is set.')
            
        else:
            raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', reading)

