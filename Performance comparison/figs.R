#!/usr/bin/env Rscript

library(ggplot2)
library(scales)

args = commandArgs(trailingOnly=TRUE)

label_log2 <- function(x) parse(text = paste0('2^', log(x, 2)))

#Function for RAM usage figure
ggplot_spsp_ram <- function()
{
  t<- read.table(args[1], h=T, sep=",")
  diskplot <- ggplot(t, aes(x=sub_rate, shape=tool_name, col=tool_name))
  gpDtotal <- diskplot + geom_point(aes(y=ram), size = 3) + labs(y="RAM usage for index\ncomparisons in Ko (log scale)", x="Subsampling rate (log scale)")+ scale_x_continuous(trans = "log2", labels = scales::math_format(2^.x, format = log2)) + scale_y_continuous(trans = "log2", labels = scales::math_format(2^.x, format = log2)) + geom_line(aes(y = ram),linetype = "solid", linewidth=2)+theme(axis.text=element_text(size=28, face="bold"),  axis.title=element_text(size=28,face="bold"), plot.title=element_text(size = 28, face = "bold"), legend.text=element_text(size=26), legend.title = element_text(size=28, face="bold"), panel.background = element_blank(), panel.grid.minor=element_line(colour="darkgray"), axis.line = element_line(colour = "black"))
  
}

#Function for disk usage figure
ggplot_spsp_disk <- function()
{
  t<- read.table(args[1], h=T, sep=",")
  diskplot <- ggplot(t, aes(x=sub_rate, shape=tool_name, color=tool_name))
  gpDtotal <- diskplot + geom_point(aes(y=disk), size = 3) + scale_fill_brewer(palette="Set3")+ scale_x_continuous(trans = "log2", labels = scales::math_format(2^.x, format = log2))+ labs(x="Subsampling rate (log scale)", y="Size of subsampled datasets\nin Mo (log scale)") + scale_y_continuous(trans = "log2", labels = scales::math_format(2^.x, format = log2)) + geom_line(aes(y = disk),linetype = "solid", linewidth=2)+theme(axis.text=element_text(size=28, face="bold"),  axis.title=element_text(size=28,face="bold"), plot.title=element_text(size = 28, face = "bold"), legend.text=element_text(size=26), legend.title = element_text(size=28, face="bold"), panel.background = element_blank(), panel.grid.minor=element_line(colour="darkgray"), axis.line = element_line(colour = "black"))
  
}

#Function for error on containment figure
ggplot_spsp_error_containment <- function()
{
  t<- read.table(args[1], h=T, sep=",")
  diskplot <- ggplot(t, aes(x=sub_rate, shape=tool_name, col=tool_name))
  gpDtotal <- diskplot + geom_point(aes(y=Error_containment), size = 3) + scale_x_continuous(trans = "log2", labels = scales::math_format(2^.x, format = log2))+ scale_y_continuous(trans = "log2", labels = scales::math_format(2^.x, format = log2))+ labs(x="Subsampling rate (log scale)", y="Error compared to SIMKA\n(log scale)") + geom_line(aes(y = Error_containment),linetype = "solid", linewidth=2)+theme(axis.text=element_text(size=28, face="bold"),  axis.title=element_text(size=28,face="bold"), plot.title=element_text(size = 28, face = "bold"), legend.text=element_text(size=26), legend.title = element_text(size=28, face="bold"), panel.background = element_blank(), panel.grid.minor=element_line(colour="darkgray"), axis.line = element_line(colour = "black"))
}

#Function for error on jaccard index figure
ggplot_spsp_error_jaccard <- function()
{
  t<- read.table(args[1], h=T, sep=",")
  diskplot <- ggplot(t, aes(x=sub_rate, shape=tool_name, col=tool_name))
  gpDtotal <- diskplot + geom_point(aes(y=Error_jaccard), size = 3) + scale_x_continuous(trans = "log2", labels = scales::math_format(2^.x, format = log2))+ scale_y_continuous(trans = "log2", labels = scales::math_format(2^.x, format = log2))+ labs(x="Subsampling rate (log scale)", y="Error compared to SIMKA\n(log scale)") + geom_line(aes(y = Error_jaccard),linetype = "solid", linewidth=2)+theme(axis.text=element_text(size=28, face="bold"),  axis.title=element_text(size=28,face="bold"), plot.title=element_text(size = 28, face = "bold"), legend.text=element_text(size=26), legend.title = element_text(size=28, face="bold"), panel.background = element_blank(), panel.grid.minor=element_line(colour="darkgray"), axis.line = element_line(colour = "black"))
}

#Function for computational time figure
ggplot_spsp_time <- function()
{
  t<- read.table(args[1], h=T, sep=",")
  diskplot <- ggplot(t, aes(x=sub_rate, shape=tool_name, col=tool_name))
  gpDtotal <- diskplot + geom_point(aes(y=time), size = 3) + labs(y="Computational time for index\ncomparisons in seconds\n(log scale)", x="Subsampling rate (log scale)")+ scale_x_continuous(trans = "log2", labels = scales::math_format(2^.x, format = log2)) + scale_y_continuous(trans = "log2", labels = scales::math_format(2^.x, format = log2)) + geom_line(aes(y = time),linetype = "solid", linewidth=2)+theme(axis.text=element_text(size=28, face="bold"),  axis.title=element_text(size=28,face="bold"), plot.title=element_text(size = 28, face = "bold"), legend.text=element_text(size=26), legend.title = element_text(size=28, face="bold"), panel.background = element_blank(), panel.grid.minor=element_line(colour="darkgray"), axis.line = element_line(colour = "black"))
}

ggsave(
  "TIME.pdf",
  ggplot_spsp_time(),
  width = 25,
  height = 7,
  dpi = 150
)

ggsave(
  "ERROR_CONTAINMENT.pdf",
  ggplot_spsp_error_containment(),
  width = 25,
  height = 7,
  dpi = 150
)

ggsave(
  "ERROR_JACCARD.pdf",
  ggplot_spsp_error_jaccard(),
  width = 25,
  height = 7,
  dpi = 150
)

ggsave(
  "SIZE.pdf",
  ggplot_spsp_disk(),
  width = 25,
  height = 7,
  dpi = 150
)

ggsave(
  "RAM.pdf",
  ggplot_spsp_ram(),
  width = 25,
  height = 7,
  dpi = 150
)