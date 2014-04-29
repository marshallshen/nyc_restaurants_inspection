#/bin/usr/ruby

require 'CSV'
require 'date'
cafes_res = []
cafe_sizes = []

def address_match?(addr1, addr2)
  addr1 && addr2 && (addr1.upcase == addr2.upcase || addr2.upcase.include?(addr1.upcase))
end

def street_match?(addr1, addr2)
  addr1 && addr2 && (addr1.upcase == addr2.upcase || addr1.upcase.include?(addr2.upcase))
end

CSV.foreach("cafes.csv", headers: true) do |row|
  cafe_sizes << row["Lic Area Sq Ft"].to_i
end

cafe_sizes.sort!
small = cafe_sizes[cafe_sizes.size / 3]
median = cafe_sizes[cafe_sizes.size / 3 * 2]
large = cafe_sizes[cafe_sizes.size-1]

#TODO: redefine the square footage range:
# Wiki average restaurants footage for NY restaurants
# Estimate better
CSV.foreach("cafes.csv", headers: true) do |row|
  size = case row["Lic Area Sq Ft"].to_i
    when (0..small)
      'smalll'
    when (small..median)
      'median'
    when (median..large)
      'large'
    end
  cafes_res << [row["Sidewalk Cafe Type"], size, row["Address Street Name"], row["Street Address"]]
end

puts "Finish processing cafes.csv"

poison_res = []
POISON_TYPES = ["Soup Kitchen", "Restaurant/Bar/Deli/Bakery", "Food Cart Vendor", "Catering Service"]
CSV.foreach("food_poisoning.csv", headers: true) do |row|

  date_string = row["Created Date"].split(" ").first
  date = Date.strptime(date_string, "%m/%d/%Y")
  freshness = case date
    when Date.parse("2014-01-01")..Date.today
      'recent'
    when Date.parse("2013-01-01")..Date.parse("2013-12-31")
      'fairly recent'
    else
      'not recent'
    end

  poison_frequency = case row['Descriptor']
     when '1 or 2'
       'occasional incidents'
     when '3 or More'
        'frequent incidents'
     end

  if POISON_TYPES.include?(row["Location Type"].to_s)
    poison_res << [row["Location Type"], poison_frequency, row['Incident Address'], row['Street Name'], freshness, row["Park Borough"]]
  end
end

puts "Finish processing food_poisoning.csv"
puts "Join two datasets..."

res = []
cafes_res.each do |cafe|
  poison_res.each do |poison|
    if address_match?(cafe[3], poison[2])
      res << [poison[0], poison[1], poison[3], poison[4], poison[5], cafe[0], cafe[1], cafe[2], "Address Match"]
    elsif street_match?(cafe[3], poison[2])
      res << [poison[0], poison[1], poison[3], poison[4], poison[5], cafe[0], cafe[1], cafe[2], "Street Match"]
    end
  end
end

CSV.open("INTEGRATED-DATASET.csv", "wb") do |csv|
  res.each do |row|
  	csv << row
  end
end